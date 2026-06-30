#!/usr/bin/env python3
"""
test_data_freshness.py — Test if data sources need refreshing.

Checks:
1. Existence of cached data files
2. Age of data files (last modified dates)
3. Availability of upstream data sources
4. Data completeness metrics
5. Recommended refresh actions

Run this periodically to ensure data is current.
"""

import json
import httpx
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# Configuration
RAW_DIR = Path("raw")
TIMEOUT = 30.0
CURRENT_YEAR = 2026
CURRENT_MONTH = 6

# Data source URLs
DATA_SOURCES = {
    "SSOC 2024 PDF": {
        "url": "https://www.singstat.gov.sg/-/media/files/standards_and_classifications/occupational_classification/ssoc2024report.ashx",
        "local_path": RAW_DIR / "ssoc2024.pdf",
        "max_age_days": 730,  # SSOC updates every few years
        "critical": True,
    },
    "SSOC 2020 PDF (fallback)": {
        "url": "https://www.singstat.gov.sg/-/media/files/standards_and_classifications/occupational_classification/ssoc2020a-detailed-definitions.ashx",
        "local_path": RAW_DIR / "ssoc2020_detailed.pdf",
        "max_age_days": 730,
        "critical": False,
    },
    "MOM Wages Page": {
        "url": "https://stats.mom.gov.sg/Pages/Occupational-Wages-Tables2024.aspx",
        "local_path": RAW_DIR / "mom_wages",
        "max_age_days": 365,  # Annual wage survey
        "critical": True,
    },
    "Employment Data API": {
        "url": "https://data.gov.sg/api/action/datastore_search",
        "local_path": RAW_DIR / "employment_by_occupation.json",
        "max_age_days": 365,  # Annual employment data
        "critical": True,
    },
}

# Processed data files
PROCESSED_FILES = {
    "occupations.json": "Parsed SSOC occupations",
    "occupations.csv": "Human-readable occupations",
    "wages.csv": "Parsed wage data",
    "employment_weights.csv": "Employment distribution estimates",
    "scores.json": "AI exposure scores (LLM-generated)",
    "docs/data.json": "Final merged visualization data",
}


class DataFreshnessReport:
    def __init__(self):
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.refresh_needed = False
        self.critical_issues = False
    
    def add_issue(self, message: str, critical: bool = False):
        self.issues.append(message)
        self.refresh_needed = True
        if critical:
            self.critical_issues = True
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def add_info(self, message: str):
        self.info.append(message)
    
    def print_report(self):
        print("\n" + "=" * 80)
        print("DATA FRESHNESS REPORT")
        print("=" * 80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current Period: {CURRENT_YEAR} Q{(CURRENT_MONTH-1)//3 + 1}")
        print("=" * 80)
        
        if self.critical_issues:
            print("\n🔴 CRITICAL ISSUES (Action Required):")
            for issue in [i for i in self.issues if "CRITICAL" in i or "missing" in i.lower()]:
                print(f"  • {issue}")
        
        if self.issues:
            print("\n⚠️  ISSUES FOUND:")
            for issue in self.issues:
                print(f"  • {issue}")
        
        if self.warnings:
            print("\n⚡ WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.info:
            print("\n✓ INFORMATION:")
            for info in self.info:
                print(f"  • {info}")
        
        print("\n" + "=" * 80)
        if self.critical_issues:
            print("RECOMMENDATION: 🔴 IMMEDIATE REFRESH REQUIRED")
            print("  Run: uv run python fetch_data.py")
        elif self.refresh_needed:
            print("RECOMMENDATION: ⚠️  REFRESH RECOMMENDED")
            print("  Run: uv run python fetch_data.py")
        else:
            print("RECOMMENDATION: ✓ Data is current, no refresh needed")
        print("=" * 80 + "\n")


def check_file_age(path: Path, max_age_days: int, name: str, report: DataFreshnessReport, critical: bool = False):
    """Check if a file exists and is within acceptable age."""
    if not path.exists():
        report.add_issue(f"{name} is MISSING: {path}", critical=critical)
        return False
    
    # Check if it's a directory
    if path.is_dir():
        files = list(path.glob("*.*"))
        if not files:
            report.add_issue(f"{name} directory is EMPTY: {path}", critical=critical)
            return False
        
        # Get newest file in directory
        newest_file = max(files, key=lambda f: f.stat().st_mtime)
        mtime = datetime.fromtimestamp(newest_file.stat().st_mtime)
        age_days = (datetime.now() - mtime).days
        
        report.add_info(f"{name}: {len(files)} files, newest from {mtime.strftime('%Y-%m-%d')} ({age_days} days old)")
        
        if age_days > max_age_days:
            report.add_warning(f"{name} is {age_days} days old (threshold: {max_age_days} days)")
            return False
        
        return True
    
    # Regular file
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    age_days = (datetime.now() - mtime).days
    size_mb = path.stat().st_size / 1_000_000
    
    report.add_info(f"{name}: {size_mb:.2f} MB, modified {mtime.strftime('%Y-%m-%d')} ({age_days} days old)")
    
    if age_days > max_age_days:
        severity = "CRITICAL" if critical else "WARNING"
        report.add_issue(f"{severity}: {name} is {age_days} days old (threshold: {max_age_days} days)", critical=critical)
        return False
    
    return True


def check_url_accessible(url: str, name: str, report: DataFreshnessReport) -> bool:
    """Check if a URL is accessible."""
    try:
        # Try HEAD request first (faster)
        for verify_ssl in [True, False]:
            try:
                with httpx.Client(timeout=TIMEOUT, follow_redirects=True, verify=verify_ssl) as client:
                    response = client.head(url, timeout=10.0)
                    if response.status_code == 200:
                        report.add_info(f"{name} URL is accessible (HTTP {response.status_code})")
                        return True
                    elif response.status_code == 405:
                        # HEAD not allowed, try GET with range
                        response = client.get(url, headers={"Range": "bytes=0-1024"}, timeout=10.0)
                        if response.status_code in [200, 206]:
                            report.add_info(f"{name} URL is accessible (HTTP {response.status_code})")
                            return True
                    
                    report.add_warning(f"{name} URL returned HTTP {response.status_code}")
                    return False
            except httpx.ConnectError as e:
                if "CERTIFICATE_VERIFY_FAILED" in str(e) and verify_ssl:
                    continue  # Retry without SSL verification
                else:
                    raise
    except httpx.TimeoutException:
        report.add_warning(f"{name} URL timed out")
        return False
    except Exception as e:
        report.add_warning(f"{name} URL check failed: {str(e)[:100]}")
        return False


def check_data_completeness(report: DataFreshnessReport):
    """Check completeness metrics of processed data."""
    
    # Check occupations.json
    occ_path = Path("occupations.json")
    if occ_path.exists():
        with open(occ_path) as f:
            occupations = json.load(f)
        report.add_info(f"Occupations: {len(occupations)} total")
        
        # Check for expected SSOC 2024 count (should be ~432-433)
        if len(occupations) < 400:
            report.add_warning(f"Occupation count ({len(occupations)}) seems low for SSOC 2024 (expected ~432)")
    
    # Check wages.csv
    wages_path = Path("wages.csv")
    if wages_path.exists():
        with open(wages_path) as f:
            wages_lines = len(f.readlines()) - 1  # Subtract header
        coverage_pct = (wages_lines / 432) * 100 if wages_lines > 0 else 0
        report.add_info(f"Wage coverage: {wages_lines}/432 occupations ({coverage_pct:.1f}%)")
        
        if coverage_pct < 40:
            report.add_warning(f"Low wage coverage ({coverage_pct:.1f}%) - consider improving matching or adding data sources")
    
    # Check employment_weights.csv
    emp_path = Path("employment_weights.csv")
    if emp_path.exists():
        with open(emp_path) as f:
            emp_lines = len(f.readlines()) - 1
        report.add_info(f"Employment weights: {emp_lines} occupations")
        
        # Parse and check total employment
        import csv
        with open(emp_path) as f:
            reader = csv.DictReader(f)
            total_emp = sum(int(row['estimated_employment']) for row in reader)
        report.add_info(f"Total employment: {total_emp:,} workers")
        
        # Singapore resident workforce should be ~2.3M in 2024-2026
        if total_emp < 2_000_000 or total_emp > 2_500_000:
            report.add_warning(f"Total employment ({total_emp:,}) outside expected range (2.0M-2.5M)")
    
    # Check scores.json
    scores_path = Path("scores.json")
    if scores_path.exists():
        with open(scores_path) as f:
            scores = json.load(f)
        report.add_info(f"AI exposure scores: {len(scores)} occupations scored")
        
        if len(scores) < 432:
            report.add_warning(f"Not all occupations scored ({len(scores)}/432)")
    
    # Check final site data
    site_data_path = Path("docs/data.json")
    if site_data_path.exists():
        with open(site_data_path) as f:
            site_data = json.load(f)
        
        # Check structure
        if "occupations" in site_data:
            occs = site_data["occupations"]
            report.add_info(f"Site data: {len(occs)} occupation records")
            
            # Check for essential fields in first occupation
            if occs:
                sample = occs[0]
                fields = ['title', 'ssoc_code', 'exposure', 'jobs']
                missing_fields = [f for f in fields if f not in sample]
                if missing_fields:
                    report.add_issue(f"Site data missing fields: {missing_fields}")
        
        # Check metadata
        if "metadata" in site_data:
            generated = site_data["metadata"].get("generated", "unknown")
            report.add_info(f"Site data generated: {generated}")
        
        # Check statistics
        if "statistics" in site_data:
            stats = site_data["statistics"]
            report.add_info(f"Statistics: {stats.get('total_occupations', 0)} occupations, {stats.get('total_workforce', 0):,} workers")


def check_current_year_data(report: DataFreshnessReport):
    """Check if we're using the most current year's data."""
    
    # Check employment data for year
    emp_path = RAW_DIR / "employment_by_occupation.json"
    if emp_path.exists():
        with open(emp_path) as f:
            emp_data = json.load(f)
        
        records = emp_data.get("result", {}).get("records", [])
        if records:
            # Check year field in records
            years = set()
            for record in records[:10]:  # Sample first 10
                year = record.get("year") or record.get("reference_year") or record.get("_id", "")[:4]
                if year:
                    years.add(str(year))
            
            if years:
                latest_year = max(years)
                report.add_info(f"Employment data year: {latest_year}")
                
                if int(latest_year) < CURRENT_YEAR - 1:
                    report.add_warning(f"Employment data is from {latest_year}, more recent data may be available")
    
    # Check MOM wages for 2025/2026 data
    wages_dir = RAW_DIR / "mom_wages"
    if wages_dir.exists():
        wage_files = list(wages_dir.glob("*.xlsx")) + list(wages_dir.glob("*.xls"))
        
        # Look for year indicators in filenames
        years_in_files = set()
        for f in wage_files:
            fname = f.name.lower()
            for year in range(2020, CURRENT_YEAR + 1):
                if str(year) in fname:
                    years_in_files.add(year)
        
        if years_in_files:
            latest_wage_year = max(years_in_files)
            report.add_info(f"Wage data year: {latest_wage_year}")
            
            if latest_wage_year < CURRENT_YEAR - 1:
                report.add_warning(f"Wage data is from {latest_wage_year}, more recent data may be available")


def main():
    print("\n🔍 Singapore Job Market Data - Freshness Test\n")
    
    report = DataFreshnessReport()
    
    # Check raw data sources
    print("Checking raw data sources...")
    for name, config in DATA_SOURCES.items():
        check_file_age(
            config["local_path"],
            config["max_age_days"],
            name,
            report,
            critical=config["critical"]
        )
        
        # Check URL accessibility (non-blocking)
        if "url" in config:
            check_url_accessible(config["url"], name, report)
    
    # Check processed files
    print("\nChecking processed data files...")
    for filename, description in PROCESSED_FILES.items():
        path = Path(filename)
        if not path.exists():
            report.add_issue(f"{description} is MISSING: {filename}")
        else:
            if path.is_file():
                size_kb = path.stat().st_size / 1000
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                report.add_info(f"{description}: {size_kb:.1f} KB, modified {mtime.strftime('%Y-%m-%d')}")
    
    # Check data completeness
    print("\nAnalyzing data completeness...")
    check_data_completeness(report)
    
    # Check for current year data
    print("\nChecking data currency...")
    check_current_year_data(report)
    
    # Print final report
    report.print_report()
    
    # Exit code
    if report.critical_issues:
        exit(1)
    elif report.refresh_needed:
        exit(2)
    else:
        exit(0)


if __name__ == "__main__":
    main()
