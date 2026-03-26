#!/usr/bin/env python3
"""
build_weights.py — Estimate employment for each detailed occupation.

Singapore publishes employment data at 2-digit SSOC level via MOM.
This script distributes those 2-digit totals to 5-digit occupations within
each sub-major group, using wage data as a proxy when available (higher pay  
= likely more employment in knowledge-intensive roles).

Outputs:
- employment_weights.csv: estimated employment per occupation
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
import openpyxl

DETAILED_EMPLOYMENT_XLSX = Path("raw/mrsd_69_Emp_Res_DetailedOcc_Sex.xlsx")
OCCUPATIONS_JSON = Path("occupations.json")
WAGES_CSV = Path("wages.csv")
OUTPUT_CSV = Path("employment_weights.csv")


def load_occupations() -> list[dict]:
    """Load SSOC occupations."""
    if not OCCUPATIONS_JSON.exists():
        print(f"✗ Error: {OCCUPATIONS_JSON} not found")
        print("  Run: uv run python parse_ssoc.py")
        return []
    
    with open(OCCUPATIONS_JSON) as f:
        return json.load(f)


def load_wages() -> dict:
    """Load wage data. Returns dict: {ssoc_code: annual_wage}"""
    wages = {}
    
    if not WAGES_CSV.exists():
        print(f"⚠ Warning: {WAGES_CSV} not found. Employment will be distributed equally.")
        return wages
    
    with open(WAGES_CSV, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wages[row['ssoc_code']] = float(row['median_annual_wage'])
    
    return wages


def load_employment_data() -> dict:
    """
    Load employment by 2-digit SSOC code from MOM detailed occupation file.
    
    The Excel file has three sections:
    - Rows 6-47: Total employment (both genders)
    - Rows 49-90: Male employment
    - Rows 92+: Female employment
    
    We only use the first section (total employment).
    
    Returns dict: {two_digit_code: employment_count}
    Example: {'11': 50300, '12': 187600, '21': 155900, ...}
    """
    if not DETAILED_EMPLOYMENT_XLSX.exists():
        print(f"✗ Error: {DETAILED_EMPLOYMENT_XLSX} not found")
        print("  Run: uv run python fetch_data.py")
        return {}
    
    wb = openpyxl.load_workbook(DETAILED_EMPLOYMENT_XLSX, data_only=True)
    sheet = wb['Sheet1']
    
    # Column 16 is 2024 data (columns are: None, None, 2011, 2012, ..., 2024, 2025)
    # Rows 6-47 contain the first section (total employment across all genders)
    # Row 48 has "Total" text which signals the end of the first section
    year_2024_col = 16
    
    employment = {}
    
    for row_idx in range(6, 48):  # Only first section
        occupation_cell = sheet.cell(row=row_idx, column=2)
        employment_cell = sheet.cell(row=row_idx, column=year_2024_col)
        
        if not occupation_cell.value or not employment_cell.value:
            continue
        
        occupation_text = str(occupation_cell.value).strip()
        
        # Skip Total row
        if occupation_text == 'Total':
            continue
        
        # Extract 2-digit code from strings like "11 Legislators, Senior Officials..."
        # Note: Some codes may be ranges like "61 - 62" or "X1 - X5"
        parts = occupation_text.split()
        if not parts or not parts[0][0].isdigit():
            continue
        
        # For codes like "11" or "61 - 62", take first code
        two_digit_code = parts[0].replace('-', '').strip()[:2]
        
        try:
            # Employment is in thousands
            employment_thousands = float(employment_cell.value)
            # If code already exists, add to it (for cases like "61 - 62")
            employment[two_digit_code] = employment.get(two_digit_code, 0) + int(employment_thousands * 1000)
        except (ValueError, TypeError):
            continue
    
    return employment


def distribute_employment(occupations: list[dict], employment: dict, wages: dict) -> list[dict]:
    """
    Distribute 2-digit SSOC employment totals to detailed 5-digit occupations.
    
    Strategy:
    - Map each 5-digit occupation to its 2-digit parent (first 2 digits of code)
    - If wage data available: weight by wage (proxy for employment)
    - Otherwise: add random variation to create realistic distribution
    """
    import random
    random.seed(42)  # Reproducible results
    
    # Group occupations by 2-digit code
    by_two_digit = defaultdict(list)
    for occ in occupations:
        two_digit = occ['ssoc_code'][:2]
        by_two_digit[two_digit].append(occ)
    
    results = []
    
    for two_digit, group_occupations in by_two_digit.items():
        total_employment = employment.get(two_digit, 0)
        
        if total_employment == 0:
            # No employment data for this 2-digit group
            # Try to get from parent 1-digit level by summing siblings
            one_digit = two_digit[0]
            
            # Sum all 2-digit groups starting with this 1-digit
            fallback_employment = sum(
                emp for code, emp in employment.items() 
                if code.startswith(one_digit)
            )
            
            if fallback_employment == 0:
                # Still no data
                for occ in group_occupations:
                    results.append({
                        'ssoc_code': occ['ssoc_code'],
                        'title': occ['title'],
                        'major_group': occ['major_group'],
                        'major_group_label': occ['major_group_label'],
                        'estimated_employment': 0,
                        'data_quality': 'no_group_data',
                    })
                continue
            
            # Distribute fallback proportionally
            total_employment = fallback_employment // 10  # Rough estimate
        
        # Calculate weights
        weights = []
        for occ in group_occupations:
            wage = wages.get(occ['ssoc_code'], 0)
            
            if wage > 0:
                # Use wage as proxy (square root to reduce skew)
                weight = wage ** 0.5
            else:
                # Fallback: random variation using log-normal distribution
                weight = random.lognormvariate(0, 1.2)
            
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        
        # Distribute employment
        for occ, weight in zip(group_occupations, weights):
            proportion = weight / total_weight if total_weight > 0 else 0
            estimated = total_employment * proportion
            
            has_wage = occ['ssoc_code'] in wages
            quality = 'two_digit_distributed_wage_weighted' if has_wage else 'two_digit_distributed_varied'
            
            results.append({
                'ssoc_code': occ['ssoc_code'],
                'title': occ['title'],
                'major_group': occ['major_group'],
                'major_group_label': occ['major_group_label'],
                'estimated_employment': round(estimated),
                'data_quality': quality,
            })
    
    return results


def save_weights(weights: list[dict]):
    """Save employment weights to CSV."""
    # Sort by SSOC code
    weights.sort(key=lambda x: x['ssoc_code'])
    
    # Save CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=weights[0].keys())
        writer.writeheader()
        writer.writerows(weights)
    
    print(f"✓ Saved {len(weights)} employment estimates to {OUTPUT_CSV}")
    
    # Statistics
    total = sum(w['estimated_employment'] for w in weights)
    with_data = sum(1 for w in weights if w['estimated_employment'] > 0)
    
    print(f"\nEmployment statistics:")
    print(f"  Total estimated employment: {total:,}")
    print(f"  Occupations with employment data: {with_data}/{len(weights)}")
    
    by_quality = defaultdict(int)
    for w in weights:
        by_quality[w['data_quality']] += 1
    
    print(f"\nData quality breakdown:")
    for quality, count in sorted(by_quality.items()):
        print(f"  {quality}: {count}")


def main():
    print("Employment Weight Builder")
    print("=" * 60)
    
    # Load occupations
    print("Loading SSOC occupations...")
    occupations = load_occupations()
    if not occupations:
        return
    print(f"✓ Loaded {len(occupations)} occupations")
    
    # Load wages
    print("\nLoading wage data...")
    wages = load_wages()
    print(f"✓ Loaded {len(wages)} wage records")
    
    # Load employment
    print("\nLoading employment data from MOM...")
    employment = load_employment_data()
    if employment:
        print(f"✓ Loaded employment data for {len(employment)} 2-digit SSOC groups (2024)")
        
        # Show first 10 groups
        print(f"\nSample groups (showing 10 of {len(employment)}):")
        for two_digit, value in sorted(employment.items())[:10]:
            print(f"  Code {two_digit}: {value:,}")
    else:
        print("⚠ No employment data loaded. Using placeholder weights.")
        # Create placeholder employment
        employment = {}
        for i in range(1, 10):
            for j in range(0, 10):
                employment[f"{i}{j}"] = 10000
    
    # Distribute employment
    print("\nDistributing employment to detailed occupations...")
    weights = distribute_employment(occupations, employment, wages)
    
    # Save outputs
    save_weights(weights)
    
    print("\n" + "=" * 60)
    print("✓ Employment weight building complete!")
    
    # Show examples
    print("\nExample employment estimates (highest):")
    top_5 = sorted(weights, key=lambda x: x['estimated_employment'], reverse=True)[:5]
    for i, w in enumerate(top_5, 1):
        print(f"{i}. {w['title']}: {w['estimated_employment']:,} ({w['data_quality']})")


if __name__ == "__main__":
    main()
