#!/usr/bin/env python3
"""
parse_wages.py — Extract and match wage data to SSOC occupations.

Reads MOM Occupational Wage Survey Excel files, extracts median wages,
and fuzzy-matches occupation titles to SSOC codes.

Outputs:
- wages.csv: median monthly/annual wages per occupation with match confidence
"""

import json
import csv
from pathlib import Path
import openpyxl
from rapidfuzz import fuzz, process

RAW_WAGES_DIR = Path("raw/mom_wages")
OCCUPATIONS_JSON = Path("occupations.json")
OUTPUT_CSV = Path("wages.csv")


def load_occupations() -> dict:
    """Load SSOC occupations. Returns dict: {ssoc_code: {title, ...}}"""
    if not OCCUPATIONS_JSON.exists():
        print(f"✗ Error: {OCCUPATIONS_JSON} not found")
        print("  Run: uv run python parse_ssoc.py")
        return {}
    
    with open(OCCUPATIONS_JSON) as f:
        occupations = json.load(f)
    
    return {occ['ssoc_code']: occ for occ in occupations}


def extract_wages_from_excel(file_path: Path) -> list[dict]:
    """
    Extract wage data from a single MOM OWS Excel file.
    
    Returns list of dicts with keys:
    - occupation_title: extracted occupation name
    - median_monthly_wage: median monthly basic wage
    """
    wages = []
    
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            
            # Look for occupation and wage columns
            # Common patterns in MOM OWS files:
            # - Column A or B: Occupation
            # - Column with "Median" or "Basic Wage": wage value
            
            # Try to find header row
            header_row = None
            occupation_col = None
            median_col = None
            
            for row_idx in range(1, min(20, sheet.max_row + 1)):  # Check first 20 rows
                row = [cell.value for cell in sheet[row_idx]]
                
                for col_idx, cell_value in enumerate(row):
                    if cell_value and isinstance(cell_value, str):
                        cell_lower = cell_value.lower()
                        
                        # Occupation column
                        if 'occupation' in cell_lower and not occupation_col:
                            occupation_col = col_idx
                            header_row = row_idx
                        
                        # Median wage column
                        if 'median' in cell_lower and 'gross' not in cell_lower:
                            if 'basic' in cell_lower or 'monthly' in cell_lower:
                                median_col = col_idx
                
                if occupation_col is not None and median_col is not None:
                    break
            
            if not (occupation_col is not None and median_col is not None):
                continue  # Skip this sheet
            
            # Extract data rows
            for row_idx in range(header_row + 1, sheet.max_row + 1):
                row = list(sheet[row_idx])
                
                occupation = row[occupation_col].value if occupation_col < len(row) else None
                wage = row[median_col].value if median_col < len(row) else None
                
                if occupation and wage:
                    try:
                        # Clean occupation title
                        occupation = str(occupation).strip()
                        
                        # Skip subtotals, headers, etc.
                        if any(skip in occupation.lower() for skip in ['total', 'average', 'note', 'n.e.c', 'overall']):
                            continue
                        
                        # Parse wage
                        wage_value = float(wage)
                        
                        if wage_value > 0:
                            wages.append({
                                'occupation_title': occupation,
                                'median_monthly_wage': wage_value,
                            })
                    except (ValueError, TypeError):
                        pass
        
        wb.close()
        
    except Exception as e:
        print(f"  Warning: Error reading {file_path.name}: {e}")
    
    return wages


def fuzzy_match_to_ssoc(wages: list[dict], occupations: dict) -> list[dict]:
    """
    Fuzzy-match wage data to SSOC occupations.
    
    Returns list of dicts with matched SSOC codes and confidence scores.
    """
    # Build lookup: list of (title, ssoc_code) for matching
    ssoc_titles = [(occ['title'], code) for code, occ in occupations.items()]
    
    matched = []
    
    for wage in wages:
        title = wage['occupation_title']
        
        # Find best match
        result = process.extractOne(
            title,
            [t[0] for t in ssoc_titles],
            scorer=fuzz.token_sort_ratio
        )
        
        if result:
            matched_title, score, idx = result
            ssoc_code = ssoc_titles[idx][1]
            
            matched.append({
                'ssoc_code': ssoc_code,
                'occupation_title': wage['occupation_title'],
                'matched_ssoc_title': matched_title,
                'median_monthly_wage': wage['median_monthly_wage'],
                'median_annual_wage': wage['median_monthly_wage'] * 12,
                'match_confidence': score / 100.0,  # Normalize to 0-1
            })
    
    return matched


def save_wages(wages: list[dict]):
    """Save wages to CSV."""
    # Sort by SSOC code
    wages.sort(key=lambda x: x['ssoc_code'])
    
    # Remove duplicates (keep highest confidence match)
    deduped = {}
    for w in wages:
        code = w['ssoc_code']
        if code not in deduped or w['match_confidence'] > deduped[code]['match_confidence']:
            deduped[code] = w
    
    wages = list(deduped.values())
    wages.sort(key=lambda x: x['ssoc_code'])
    
    # Save CSV
    if wages:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=wages[0].keys())
            writer.writeheader()
            writer.writerows(wages)
        print(f"✓ Saved {len(wages)} wage records to {OUTPUT_CSV}")
    
    # Statistics
    avg_confidence = sum(w['match_confidence'] for w in wages) / len(wages) if wages else 0
    print(f"\nMatch statistics:")
    print(f"  Average confidence: {avg_confidence:.2%}")
    print(f"  High confidence (>0.8): {sum(1 for w in wages if w['match_confidence'] > 0.8)}")
    print(f"  Medium confidence (0.6-0.8): {sum(1 for w in wages if 0.6 <= w['match_confidence'] <= 0.8)}")
    print(f"  Low confidence (<0.6): {sum(1 for w in wages if w['match_confidence'] < 0.6)}")


def main():
    print("MOM Wage Data Parser")
    print("=" * 60)
    
    # Load SSOC occupations
    print("Loading SSOC occupations...")
    occupations = load_occupations()
    if not occupations:
        return
    print(f"✓ Loaded {len(occupations)} SSOC occupations")
    
    # Check for wage files
    if not RAW_WAGES_DIR.exists():
        print(f"✗ Error: {RAW_WAGES_DIR} not found")
        print("  Run: uv run python fetch_data.py")
        return
    
    wage_files = list(RAW_WAGES_DIR.glob("*.xlsx")) + list(RAW_WAGES_DIR.glob("*.xls"))
    
    if not wage_files:
        print(f"✗ Error: No Excel files found in {RAW_WAGES_DIR}")
        print("  Run: uv run python fetch_data.py")
        return
    
    print(f"\nFound {len(wage_files)} wage files")
    
    # Extract wages from all files
    all_wages = []
    for i, file_path in enumerate(wage_files, 1):
        print(f"[{i}/{len(wage_files)}] Parsing {file_path.name}...")
        wages = extract_wages_from_excel(file_path)
        all_wages.extend(wages)
        print(f"  ✓ Extracted {len(wages)} wage entries")
    
    print(f"\n✓ Total wage entries extracted: {len(all_wages)}")
    
    if not all_wages:
        print("⚠ No wage data extracted. Manual intervention may be required.")
        return
    
    # Fuzzy match to SSOC
    print("\nMatching wages to SSOC occupations...")
    matched = fuzzy_match_to_ssoc(all_wages, occupations)
    
    # Save outputs
    save_wages(matched)
    
    print("\n" + "=" * 60)
    print("✓ Wage parsing complete!")
    
    # Show examples
    if matched:
        print("\nExample wage matches:")
        for i, w in enumerate(matched[:5]):
            print(f"\n{i+1}. {w['matched_ssoc_title']} ({w['ssoc_code']})")
            print(f"   MOM title: {w['occupation_title']}")
            print(f"   Monthly: ${w['median_monthly_wage']:,.0f} | Annual: ${w['median_annual_wage']:,.0f}")
            print(f"   Match confidence: {w['match_confidence']:.1%}")


if __name__ == "__main__":
    main()
