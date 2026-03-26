#!/usr/bin/env python3
"""
parse_ssoc.py — Extract structured occupation data from SSOC 2024 PDF.

Parses the SSOC 2024 report to extract:
- 5-digit SSOC codes
- Occupation titles
- Task/duty descriptions
- Major and sub-major group classifications

Outputs:
- occupations.json (machine-readable)
- occupations.csv (human-readable)
"""

import json
import csv
import re
from pathlib import Path
import pdfplumber

RAW_DIR = Path("raw")
SSOC_2024_PATH = RAW_DIR / "ssoc2024.pdf"
SSOC_2020_PATH = RAW_DIR / "ssoc2020_detailed.pdf"

OUTPUT_JSON = Path("occupations.json")
OUTPUT_CSV = Path("occupations.csv")

# SSOC 2024 major groups
MAJOR_GROUPS = {
    "1": "Managers",
    "2": "Professionals",
    "3": "Technicians and Associate Professionals",
    "4": "Clerical Support Workers",
    "5": "Service and Sales Workers",
    "6": "Skilled Agricultural, Forestry, and Fishery Workers",
    "7": "Craft and Related Trades Workers",
    "8": "Plant and Machine Operators and Assemblers",
    "9": "Elementary Occupations",
}


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def extract_occupations_from_pdf(pdf_path: Path) -> list[dict]:
    """
    Extract occupation entries from SSOC PDF.
    
    Returns list of dicts with keys:
    - ssoc_code: 5-digit code (e.g., "21111")
    - title: occupation title
    - description: task/duty description
    - major_group: 1-digit major group
    - sub_major: 2-digit sub-major group
    """
    occupations = []
    
    print(f"Opening PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        full_text = ""
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Pattern to match occupation entries
        # Typical format:
        # 21111 Mathematician
        # Description text...
        # or
        # 2111 Mathematicians, Statisticians and Actuaries
        # 21111 Mathematician
        # Task description...
        
        # Split by lines and process
        lines = full_text.split('\n')
        
        current_code = None
        current_title = None
        current_description = []
        
        for line in lines:
            line = line.strip()
            
            # Match 5-digit code at start of line
            match = re.match(r'^(\d{5})\s+(.+)', line)
            
            if match:
                # Save previous occupation if exists
                if current_code and current_title:
                    description = ' '.join(current_description).strip()
                    if description:  # Only add if we have a description
                        occupations.append({
                            'ssoc_code': current_code,
                            'title': current_title,
                            'description': description,
                        })
                
                # Start new occupation
                current_code = match.group(1)
                current_title = match.group(2).strip()
                current_description = []
                
            elif current_code:
                # Continuation of description
                # Skip lines that look like headers or page numbers
                if line and not re.match(r'^(Page \d+|SSOC|Singapore Standard)', line):
                    # Skip sub-group headers (4-digit codes without titles on same line)
                    if not re.match(r'^\d{4}$', line):
                        current_description.append(line)
        
        # Add final occupation
        if current_code and current_title:
            description = ' '.join(current_description).strip()
            if description:
                occupations.append({
                    'ssoc_code': current_code,
                    'title': current_title,
                    'description': description,
                })
    
    print(f"✓ Extracted {len(occupations)} occupations from PDF")
    return occupations


def enrich_occupation(occ: dict) -> dict:
    """Add derived fields to occupation."""
    code = occ['ssoc_code']
    
    # Major group (first digit)
    major_group = code[0]
    
    # Sub-major group (first 2 digits)
    sub_major = code[:2]
    
    # Major group label
    major_group_label = MAJOR_GROUPS.get(major_group, "Unknown")
    
    # Slug for URL
    slug = slugify(occ['title'])
    
    return {
        'ssoc_code': code,
        'title': occ['title'],
        'major_group': major_group,
        'major_group_label': major_group_label,
        'sub_major': sub_major,
        'description': occ['description'],
        'slug': slug,
    }


def save_occupations(occupations: list[dict]):
    """Save occupations to JSON and CSV."""
    # Sort by SSOC code
    occupations.sort(key=lambda x: x['ssoc_code'])
    
    # Save JSON
    OUTPUT_JSON.write_text(json.dumps(occupations, indent=2, ensure_ascii=False))
    print(f"✓ Saved {len(occupations)} occupations to {OUTPUT_JSON}")
    
    # Save CSV
    if occupations:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=occupations[0].keys())
            writer.writeheader()
            writer.writerows(occupations)
        print(f"✓ Saved {len(occupations)} occupations to {OUTPUT_CSV}")
    
    # Print summary by major group
    print("\nOccupations by major group:")
    from collections import Counter
    counts = Counter(occ['major_group'] for occ in occupations)
    for group in sorted(counts.keys()):
        label = MAJOR_GROUPS.get(group, "Unknown")
        print(f"  {group} — {label}: {counts[group]}")


def main():
    print("SSOC Occupation Parser")
    print("=" * 60)
    
    # Check which PDF exists
    pdf_path = None
    if SSOC_2024_PATH.exists():
        pdf_path = SSOC_2024_PATH
        print(f"Using SSOC 2024: {pdf_path}")
    elif SSOC_2020_PATH.exists():
        pdf_path = SSOC_2020_PATH
        print(f"⚠ SSOC 2024 not found, using SSOC 2020 fallback: {pdf_path}")
    else:
        print(f"✗ Error: No SSOC PDF found")
        print(f"  Expected: {SSOC_2024_PATH} or {SSOC_2020_PATH}")
        print(f"  Run: uv run python fetch_data.py")
        return
    
    # Extract occupations
    raw_occupations = extract_occupations_from_pdf(pdf_path)
    
    if not raw_occupations:
        print("\n⚠ Warning: No occupations extracted!")
        print("  The PDF format may have changed.")
        print("  Manual intervention required.")
        return
    
    # Enrich with metadata
    occupations = [enrich_occupation(occ) for occ in raw_occupations]
    
    # Save outputs
    save_occupations(occupations)
    
    print("\n" + "=" * 60)
    print("✓ SSOC parsing complete!")
    
    # Show examples
    print("\nExample occupations:")
    for i, occ in enumerate(occupations[:3]):
        print(f"\n{i+1}. {occ['title']} ({occ['ssoc_code']})")
        print(f"   Group: {occ['major_group_label']}")
        print(f"   Description: {occ['description'][:100]}...")


if __name__ == "__main__":
    main()
