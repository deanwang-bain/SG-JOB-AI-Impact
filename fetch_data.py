#!/usr/bin/env python3
"""
fetch_data.py — Download and cache raw data sources.

Downloads:
- SSOC 2024 PDF from SingStat
- MOM Occupational Wage Survey 2024 Excel files
- Employment by occupation from data.gov.sg API

All files cached in raw/ directory. Skips re-downloading if already present.
"""

import httpx
import json
import time
from pathlib import Path
from bs4 import BeautifulSoup

# Configuration
RAW_DIR = Path("raw")
RAW_DIR.mkdir(exist_ok=True)
(RAW_DIR / "mom_wages").mkdir(exist_ok=True)

TIMEOUT = 30.0

# Data sources
SSOC_2024_URL = "https://www.singstat.gov.sg/-/media/files/standards_and_classifications/occupational_classification/ssoc2024report.ashx"
SSOC_2024_PATH = RAW_DIR / "ssoc2024.pdf"

# Fallback: SSOC 2020 detailed definitions (cleaner format if 2024 fails)
SSOC_2020_URL = "https://www.singstat.gov.sg/-/media/files/standards_and_classifications/occupational_classification/ssoc2020a-detailed-definitions.ashx"
SSOC_2020_PATH = RAW_DIR / "ssoc2020_detailed.pdf"

MOM_WAGES_PAGE = "https://stats.mom.gov.sg/Pages/Occupational-Wages-Tables2024.aspx"
MOM_WAGES_DIR = RAW_DIR / "mom_wages"

EMPLOYMENT_API = "https://data.gov.sg/api/action/datastore_search"
EMPLOYMENT_RESOURCE_ID = "d_1d7ab908d16d7b9ddf6f2c2985894119"
EMPLOYMENT_PATH = RAW_DIR / "employment_by_occupation.json"


def download_file(url: str, path: Path, description: str, required: bool = True):
    """Download a file if it doesn't exist locally."""
    if path.exists():
        print(f"✓ {description} already cached at {path}")
        return True
    
    print(f"Downloading {description}...")
    print(f"  URL: {url}")
    
    # Try with SSL verification first, then without if it fails
    for verify_ssl in [True, False]:
        try:
            with httpx.Client(timeout=TIMEOUT, follow_redirects=True, verify=verify_ssl) as client:
                response = client.get(url)
                response.raise_for_status()
                
                path.write_bytes(response.content)
                size_mb = len(response.content) / 1_000_000
                print(f"✓ Downloaded {size_mb:.2f} MB → {path}")
                return True
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e) and verify_ssl:
                print(f"  ⚠ SSL verification failed, retrying without verification...")
                continue
            else:
                if required:
                    print(f"✗ Error downloading {description}: {e}")
                    raise
                else:
                    print(f"⚠ Could not download {description}: {e}")
                    return False
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                if required:
                    print(f"✗ File not found (404): {description}")
                    raise
                else:
                    print(f"⚠ File not found (404): {description}")
                    return False
            else:
                if required:
                    print(f"✗ HTTP error downloading {description}: {e}")
                    raise
                else:
                    print(f"⚠ HTTP error downloading {description}: {e}")
                    return False
        except Exception as e:
            if required:
                print(f"✗ Error downloading {description}: {e}")
                raise
            else:
                print(f"⚠ Error downloading {description}: {e}")
                return False
    
    return False


def fetch_ssoc():
    """Download SSOC 2024 PDF and fallback SSOC 2020."""
    print("\n=== SSOC Occupational Classification ===")
    
    # Try SSOC 2024 first (may not be available yet)
    success_2024 = download_file(SSOC_2024_URL, SSOC_2024_PATH, "SSOC 2024 report", required=False)
    
    # Download SSOC 2020 as fallback if SSOC 2024 doesn't exist
    if not SSOC_2024_PATH.exists():
        download_file(SSOC_2020_URL, SSOC_2020_PATH, "SSOC 2020 detailed definitions", required=True)
        print("  Note: SSOC 2024 not available, will use SSOC 2020 for parsing")
    else:
        print("  ✓ SSOC 2024 available")
        # Try to download SSOC 2020 as supplementary reference, but don't require it
        download_file(SSOC_2020_URL, SSOC_2020_PATH, "SSOC 2020 detailed definitions (reference)", required=False)


def fetch_mom_wages():
    """Scrape MOM wage survey page and download Excel files."""
    print("\n=== MOM Occupational Wage Survey 2024 ===")
    
    # First, check if we already have files
    existing_files = list(MOM_WAGES_DIR.glob("*.xlsx")) + list(MOM_WAGES_DIR.glob("*.xls"))
    if existing_files:
        print(f"✓ Found {len(existing_files)} existing wage files in {MOM_WAGES_DIR}")
        for f in existing_files:
            print(f"  - {f.name}")
        return
    
    print(f"Fetching {MOM_WAGES_PAGE}...")
    
    try:
        # Try with and without SSL verification
        soup = None
        client_to_use = None
        
        for verify_ssl in [True, False]:
            try:
                client_to_use = httpx.Client(timeout=TIMEOUT, follow_redirects=True, verify=verify_ssl)
                response = client_to_use.get(MOM_WAGES_PAGE)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                break  # Success, exit retry loop
            except httpx.ConnectError as e:
                if "CERTIFICATE_VERIFY_FAILED" in str(e) and verify_ssl:
                    print(f"  ⚠ SSL verification failed, retrying without verification...")
                    if client_to_use:
                        client_to_use.close()
                    continue
                else:
                    if client_to_use:
                        client_to_use.close()
                    raise
        
        if not soup:
            raise Exception("Failed to fetch MOM wages page")
        
        # Find all links to Excel files
        excel_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith(('.xlsx', '.xls', '.XLSX', '.XLS')):
                # Convert relative to absolute URL
                if href.startswith('http'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = f"https://stats.mom.gov.sg{href}"
                else:
                    full_url = f"https://stats.mom.gov.sg/{href}"
                
                excel_links.append((full_url, link.get_text(strip=True)))
        
        if not excel_links:
            print("⚠ No Excel files found on MOM wages page")
            print("  This may require manual intervention or the page structure changed")
            if client_to_use:
                client_to_use.close()
            return
        
        print(f"Found {len(excel_links)} Excel files")
        
        # Download each file  
        for i, (url, title) in enumerate(excel_links):
            # Generate filename from URL
            filename = url.split('/')[-1].split('?')[0]
            
            # Clean filename
            if not filename.endswith(('.xlsx', '.xls')):
                filename = f"wages_table_{i+1}.xlsx"
            
            filepath = MOM_WAGES_DIR / filename
            
            if filepath.exists():
                print(f"  ✓ {filename} already exists")
                continue
            
            print(f"  [{i+1}/{len(excel_links)}] Downloading {filename}...")
            
            try:
                resp = client_to_use.get(url)
                resp.raise_for_status()
                filepath.write_bytes(resp.content)
                print(f"    ✓ {len(resp.content) / 1000:.1f} KB")
                time.sleep(0.5)  # Rate limit
            except Exception as e:
                print(f"    ✗ Error: {e}")
        
        if client_to_use:
            client_to_use.close()
        
        print(f"✓ Downloaded wage files to {MOM_WAGES_DIR}")
        
    except Exception as e:
        print(f"✗ Error fetching MOM wages: {e}")
        print("  You may need to manually download from:")
        print(f"  {MOM_WAGES_PAGE}")


def fetch_employment():
    """Download employment by occupation from data.gov.sg API."""
    print("\n=== Employment by Occupation (data.gov.sg) ===")
    
    if EMPLOYMENT_PATH.exists():
        print(f"✓ Employment data already cached at {EMPLOYMENT_PATH}")
        return
    
    print(f"Fetching from data.gov.sg API...")
    
    try:
        # Try with and without SSL verification
        for verify_ssl in [True, False]:
            try:
                with httpx.Client(timeout=TIMEOUT, verify=verify_ssl) as client:
                    params = {
                        "resource_id": EMPLOYMENT_RESOURCE_ID,
                        "limit": 5000  # Get all records
                    }
                    
                    response = client.get(EMPLOYMENT_API, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if not data.get("success"):
                        print(f"✗ API returned success=false: {data}")
                        return
                    
                    records = data.get("result", {}).get("records", [])
                    print(f"✓ Downloaded {len(records)} employment records")
                    
                    # Save the full API response
                    EMPLOYMENT_PATH.write_text(json.dumps(data, indent=2))
                    print(f"✓ Saved to {EMPLOYMENT_PATH}")
                    return
            except httpx.ConnectError as e:
                if "CERTIFICATE_VERIFY_FAILED" in str(e) and verify_ssl:
                    print(f"  ⚠ SSL verification failed, retrying without verification...")
                    continue
                else:
                    raise
    except Exception as e:
        print(f"✗ Error fetching employment data: {e}")
        raise


def main():
    print("Singapore Job Market Data Fetcher")
    print("=" * 60)
    
    fetch_ssoc()
    fetch_mom_wages()
    fetch_employment()
    
    print("\n" + "=" * 60)
    print("✓ Data fetch complete!")
    print(f"\nRaw data cached in: {RAW_DIR.absolute()}")
    
    # Print summary
    print("\nSummary:")
    if SSOC_2024_PATH.exists():
        print(f"  ✓ SSOC 2024: {SSOC_2024_PATH.stat().st_size / 1_000_000:.2f} MB")
    if SSOC_2020_PATH.exists():
        print(f"  ✓ SSOC 2020 (fallback): {SSOC_2020_PATH.stat().st_size / 1_000_000:.2f} MB")
    
    wage_files = list(MOM_WAGES_DIR.glob("*.xlsx")) + list(MOM_WAGES_DIR.glob("*.xls"))
    if wage_files:
        print(f"  ✓ MOM wage files: {len(wage_files)} files")
    
    if EMPLOYMENT_PATH.exists():
        print(f"  ✓ Employment data: {EMPLOYMENT_PATH.stat().st_size / 1000:.1f} KB")


if __name__ == "__main__":
    main()
