#!/usr/bin/env python3
"""
build_site_data.py — Merge all data sources into final visualization dataset.

Combines:
- SSOC occupations
- AI exposure scores
- Wage data
- Employment estimates

Outputs:
- docs/data.json: complete dataset for treemap visualization
"""

import json
import csv
import re
from pathlib import Path

OCCUPATIONS_JSON = Path("occupations.json")
SCORES_JSON = Path("scores.json")
WAGES_CSV = Path("wages.csv")
EMPLOYMENT_CSV = Path("employment_weights.csv")

SITE_DIR = Path("docs")
OUTPUT_JSON = SITE_DIR / "data.json"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def extract_education(description: str) -> str:
    """
    Extract education level from occupation description.
    
    Simple heuristic based on common keywords.
    """
    desc_lower = description.lower()
    
    if any(word in desc_lower for word in ['doctoral', 'phd', 'doctorate']):
        return "Doctoral degree"
    elif any(word in desc_lower for word in ['master', 'postgraduate']):
        return "Master's degree"
    elif any(word in desc_lower for word in ['bachelor', 'degree', 'university', 'graduate']):
        return "Bachelor's degree"
    elif any(word in desc_lower for word in ['diploma', 'polytechnic', 'associate']):
        return "Diploma"
    elif any(word in desc_lower for word in ['certificate', 'vocational', 'ite']):
        return "Certificate"
    else:
        # Default based on major group
        return "Secondary"


def load_data():
    """Load all data sources."""
    # Occupations
    if not OCCUPATIONS_JSON.exists():
        print(f"✗ Error: {OCCUPATIONS_JSON} not found")
        return None
    
    with open(OCCUPATIONS_JSON) as f:
        occupations = {occ['ssoc_code']: occ for occ in json.load(f)}
    
    # Scores
    scores = {}
    if SCORES_JSON.exists():
        with open(SCORES_JSON) as f:
            scores = {s['ssoc_code']: s for s in json.load(f)}
    else:
        print(f"⚠ Warning: {SCORES_JSON} not found. AI exposure will be null.")
    
    # Wages
    wages = {}
    if WAGES_CSV.exists():
        with open(WAGES_CSV, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                wages[row['ssoc_code']] = float(row['median_annual_wage'])
    else:
        print(f"⚠ Warning: {WAGES_CSV} not found. Pay will be null.")
    
    # Employment
    employment = {}
    if EMPLOYMENT_CSV.exists():
        with open(EMPLOYMENT_CSV, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                employment[row['ssoc_code']] = int(row['estimated_employment'])
    else:
        print(f"⚠ Warning: {EMPLOYMENT_CSV} not found. Jobs will be null.")
    
    return occupations, scores, wages, employment


def build_site_data(occupations, scores, wages, employment):
    """Build final dataset for visualization."""
    data = []
    
    for code, occ in occupations.items():
        # Get score
        score = scores.get(code, {})
        exposure = score.get('exposure')
        rationale = score.get('rationale', '')
        
        # Get wage
        pay = wages.get(code)
        
        # Get employment
        jobs = employment.get(code)
        
        # Extract education
        education = extract_education(occ['description'])
        
        # Build entry
        entry = {
            'ssoc_code': code,
            'title': occ['title'],
            'slug': occ['slug'],
            'major_group': occ['major_group'],
            'category': slugify(occ['major_group_label']),
            'category_label': occ['major_group_label'],
            'pay': pay,
            'jobs': jobs,
            'education': education,
            'exposure': exposure,
            'exposure_rationale': rationale,
            'ssoc_url': "https://go.gov.sg/ssoc-search-engine",
        }
        
        data.append(entry)
    
    # Sort by SSOC code
    data.sort(key=lambda x: x['ssoc_code'])
    
    return data


def calculate_statistics(data):
    """Calculate summary statistics."""
    stats = {
        'total_occupations': len(data),
        'total_workforce': 0,
        'avg_exposure': 0,
        'scored_occupations': 0,
        'with_pay': 0,
        'with_employment': 0,
    }
    
    # Workforce
    jobs = [d['jobs'] for d in data if d['jobs']]
    if jobs:
        stats['total_workforce'] = sum(jobs)
        stats['with_employment'] = len(jobs)
    
    # Pay
    stats['with_pay'] = sum(1 for d in data if d['pay'])
    
    # Exposure
    exposures = [d['exposure'] for d in data if d['exposure'] is not None]
    if exposures:
        stats['avg_exposure'] = sum(exposures) / len(exposures)
        stats['scored_occupations'] = len(exposures)
        
        # Weighted average by employment
        weighted_sum = 0
        total_weight = 0
        for d in data:
            if d['exposure'] is not None and d['jobs']:
                weighted_sum += d['exposure'] * d['jobs']
                total_weight += d['jobs']
        
        if total_weight > 0:
            stats['weighted_avg_exposure'] = weighted_sum / total_weight
    
    # PME analysis (major groups 1, 2, 3)
    pme_jobs = sum(d['jobs'] or 0 for d in data if d['major_group'] in ['1', '2', '3'])
    pme_exposures = [d['exposure'] for d in data if d['major_group'] in ['1', '2', '3'] and d['exposure'] is not None]
    
    stats['pme_workforce'] = pme_jobs
    stats['pme_share'] = pme_jobs / stats['total_workforce'] if stats['total_workforce'] > 0 else 0
    stats['pme_avg_exposure'] = sum(pme_exposures) / len(pme_exposures) if pme_exposures else 0
    
    return stats


def save_site_data(data, stats):
    """Save final dataset to site directory."""
    SITE_DIR.mkdir(exist_ok=True)
    
    output = {
        'metadata': {
            'generated': '2026-03-26',
            'version': '1.0',
            'sources': [
                'SSOC 2024 (SingStat)',
                'MOM Occupational Wage Survey 2024',
                'data.gov.sg Employment Dataset',
                'OpenAI GPT-4o AI Exposure Scoring',
            ],
        },
        'statistics': stats,
        'occupations': data,
    }
    
    OUTPUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"✓ Saved {len(data)} occupations to {OUTPUT_JSON}")


def main():
    print("Site Data Builder")
    print("=" * 60)
    
    # Load all data
    print("Loading data sources...")
    result = load_data()
    if not result:
        return
    
    occupations, scores, wages, employment = result
    
    print(f"✓ Loaded {len(occupations)} occupations")
    print(f"✓ Loaded {len(scores)} AI exposure scores")
    print(f"✓ Loaded {len(wages)} wage records")
    print(f"✓ Loaded {len(employment)} employment estimates")
    
    # Build dataset
    print("\nBuilding final dataset...")
    data = build_site_data(occupations, scores, wages, employment)
    
    # Calculate statistics
    print("Calculating statistics...")
    stats = calculate_statistics(data)
    
    # Save output
    save_site_data(data, stats)
    
    print("\n" + "=" * 60)
    print("✓ Site data build complete!")
    
    # Print summary
    print("\nDataset summary:")
    print(f"  Total occupations: {stats['total_occupations']}")
    print(f"  Scored: {stats['scored_occupations']} ({stats['scored_occupations']/stats['total_occupations']*100:.1f}%)")
    print(f"  With pay data: {stats['with_pay']} ({stats['with_pay']/stats['total_occupations']*100:.1f}%)")
    print(f"  With employment data: {stats['with_employment']} ({stats['with_employment']/stats['total_occupations']*100:.1f}%)")
    
    if stats['total_workforce'] > 0:
        print(f"\nWorkforce statistics:")
        print(f"  Total estimated workforce: {stats['total_workforce']:,}")
        print(f"  PME workforce: {stats['pme_workforce']:,} ({stats['pme_share']*100:.1f}%)")
    
    if stats['avg_exposure'] > 0:
        print(f"\nAI Exposure:")
        print(f"  Average (unweighted): {stats['avg_exposure']:.2f}/10")
        if stats.get('weighted_avg_exposure'):
            print(f"  Average (job-weighted): {stats['weighted_avg_exposure']:.2f}/10")
        if stats['pme_avg_exposure'] > 0:
            print(f"  PME average: {stats['pme_avg_exposure']:.2f}/10")
    
    print(f"\n✓ Ready for visualization!")
    print(f"  cd site && python -m http.server 8000")


if __name__ == "__main__":
    main()
