# Singapore Job Market AI Impact Visualizer

A Singapore version of [Andrej Karpathy's US Job Market Visualizer](https://karpathy.ai/jobs/), analyzing AI exposure across 441 Singapore occupations using government data sources and enhanced modeling.

**🌐 Live Demo**: [Your GitHub Pages URL will be here]

## Features

- **Comprehensive occupation coverage**: 441 detailed SSOC 2020 occupations
- **Enriched employment data**: Hybrid model combining MOM 2-digit real data + high-confidence registration overrides + multi-factor distribution
- **High-quality professional counts**: ~110K workers (4.6%) from mandatory registrations (doctors, nurses, teachers, lawyers, police)
- **LLM-powered AI exposure scoring**: Uses OpenAI GPT-4o to rate each occupation's AI exposure (0-10 scale)
- **Interactive treemap**: Visualize jobs by AI exposure, pay, education level, or major group
- **Adjustable view**: Slider to show top 10-441 jobs by employment
- **Singapore-specific insights**: PME exposure analysis (65.2% of workforce)

## Data Sources

### Employment Data (Option 3: Enriched Model)
1. **MOM Labour Force Survey 2024** — 2-digit SSOC employment (41 categories, 2.38M residents) - PRIMARY BASELINE
2. **MOH Health Manpower Statistics** — Registered healthcare professionals (doctors: 17,582, nurses: 46,344, etc.)
3. **MOE Education Statistics** — Teachers by level (primary: 15,273, secondary: 12,353)
4. **Law Society of Singapore** — Practicing lawyers (6,273)
5. **Singapore Police Force** — Regular officers (10,500)
6. **MOM Job Vacancy Survey 2024** — Detailed occupation demand data for distribution weights

### Other Data
7. **SSOC 2020** — Occupation definitions and task descriptions
8. **MOM Occupational Wage Survey 2024** — Median wages
9. **OpenAI GPT-4o** — AI exposure scoring calibrated for Singapore context

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key (for LLM scoring)

### Installation

```bash
# Install dependencies
uv sync

# Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### 0. Test data freshness (optional but recommended)
```bash
python3 test_data_freshness.py
```
Checks if cached data needs refreshing. See [TESTING.md](TESTING.md) for details.

Run the pipeline in order:

### 1. Fetch raw data
```bash
uv run python fetch_data.py
```
Downloads and caches:
- SSOC 2024 PDF → `raw/ssoc2024.pdf`
- MOM wage tables → `raw/mom_wages/*.xlsx`
- Employment data → `raw/employment_by_occupation.json`

### 2. Parse SSOC occupations
```bash
uv run python parse_ssoc.py
```
Extracts structured occupation data:
- `occupations.json` — machine-readable format
- `occupations.csv` — human-readable inspection

### 3. Parse wage data
```bash
uv run python parse_wages.py
```
Extracts and fuzzy-matches wages to SSOC codes:
- `wages.csv` — median monthly/annual wages per occupation

### 4. Build employment weights (Option 3: Enriched Model)
```bash
uv run python build_option3.py
```
Builds enriched employment model combining:
- MOM 2-digit baseline (100% real)
- Registration overrides (~110K workers with perfect data)
- Multi-factor distribution (wage + vacancy + uniform weights)
- Exact calibration to MOM 2-digit totals

Outputs:
- `employment_weights_option3.csv` — estimated employment per occupation with confidence scores

### 5. Score AI exposure (LLM)
```bash
uv run python score.py
```
**This is the longest step** (~432 API calls, ~5-10 minutes with rate limiting).
- Checkpoint after each occupation → `scores.json`
- Resumable if interrupted
- Cost estimate: ~$2-3 on GPT-4o

### 6. Build final site data
```bash
uv run python build_site_data.py
```
Merges all sources into:
- `site/data.json` — complete dataset for visualization

### 7. View the visualization
```bash
cd docs
python -m http.server 8000
```
Open http://localhost:8000 in your browser.

## Data Quality & Methodology

### Employment Data Quality (Option 3)

Our hybrid approach combines multiple data sources with varying confidence levels:

| Confidence | Source | Occupations | % of Workforce |
|-----------|--------|-------------|----------------|
| ★★★★★ Very High | Mandatory registrations (MOH, MOE, Law Society, SPF) | ~50 | 4.6% |
| ★★★★☆ High | Multi-factor model validated against pipelines | ~100 | 30% |
| ★★★☆☆ Medium | Wage-weighted distribution, calibrated to MOM | ~250 | 50% |
| ★★☆☆☆ Low | Equal distribution where data insufficient | ~41 | 15.4% |

**Key Benefits:**
- ✅ 100% accuracy at 2-digit aggregate level (exactly matches MOM official data)
- ✅ ~110,000 workers with perfect registration counts
- ✅ Eliminates absurdities (validated against Singapore context)
- ✅ Transparent confidence scoring for each occupation

### Known Limitations

⚠️ **Most employment counts are modeled**: Only ~110K (4.6%) are from direct registrations. Remaining 95.4% distributed using multi-factor weights (wage, vacancy, uniform). Not actual 5-digit SSOC counts from surveys.

⚠️ **5-digit SSOC data doesn't exist publicly**: Singapore publishes employment at 2-digit only. We searched 50+ sources (see `DATA_SOURCE_ENRICHMENT_2026.md`).

⚠️ **No projections**: Unlike US BLS, Singapore doesn't publish 10-year occupation growth projections.

⚠️ **Resident workers only**: Covers ~2.38M resident workers (citizens and PRs), excluding non-resident workforce (~30% of total).

⚠️ **AI exposure is subjective**: Scores reflect GPT-4o's assessment using the provided rubric, calibrated for Singapore's context.

**💡 Want to understand our data sources?** See [DATA_SOURCE_ENRICHMENT_2026.md](DATA_SOURCE_ENRICHMENT_2026.md) for comprehensive analysis of 50+ potential sources and [CHANGELOG.md](CHANGELOG.md) for evolution of our approach.

## Project Structure

```
.
├── fetch_data.py                  # Download raw data sources
├── parse_ssoc.py                  # Extract occupations from SSOC PDF
├── parse_wages.py                 # Extract and match wage data
├── build_option3.py               # Build enriched employment model ⭐ NEW
├── score.py                       # LLM scoring pipeline
├── build_site_data.py             # Merge all data sources
├── test_data_freshness.py         # Automated data quality checks
├── raw/                           # Cached raw data (gitignored)
│   ├── ssoc2020_report.pdf
│   ├── mrsd_69_Emp_Res_DetailedOcc_Sex.xlsx
│   └── mom_wages/*.xlsx
├── occupations.json               # Parsed SSOC occupations
├── occupations.csv                # (Human-readable)
├── wages.csv                      # Parsed wage data
├── employment_weights_option3.csv # Enriched employment estimates ⭐
├── scores.json                    # LLM AI exposure scores
├── docs/
│   ├── index.html                 # Interactive visualization
│   └── data.json                  # Final merged dataset
├── DATA_SOURCE_ENRICHMENT_2026.md # Comprehensive data source analysis
├── DATA_ENRICHMENT_SUMMARY.md     # Executive summary
├── CHANGELOG.md                   # Project history and decisions
├── TESTING.md                     # Data freshness testing guide
└── README.md                      # This file
```

## Data Quality and Maintenance

### Testing Data Freshness

To check if your data sources need refreshing:

```bash
python3 test_data_freshness.py
```

This automated test checks:
- Existence and age of all data files
- Accessibility of upstream data sources (MOM, SingStat, data.gov.sg)
- Data completeness metrics (wage coverage, employment totals)
- Data quality indicators

See [TESTING.md](TESTING.md) for detailed documentation on interpreting results and troubleshooting.

### Understanding Our Data Sources

We conducted extensive research (50+ sources) to find the best available data:

**Searched:**
- Government agencies: MOM, MOH, MOE, MHA, CPF, IRAS, WSG, SkillsFuture
- Professional bodies: Medical Council, Nursing Board, Law Society, ISCA, IES
- Industry sources: BCA, MPA, ACRA, enterprise surveys
- Alternative: LinkedIn, job postings, education pipeline

**Key Finding:** No 5-digit SSOC employment data exists publicly in Singapore. MOM publishes 2-digit only.

**Solution:** Option 3 hybrid model using registration data where available + enhanced multi-factor distribution.

See comprehensive analysis:
- [DATA_SOURCE_ENRICHMENT_2026.md](DATA_SOURCE_ENRICHMENT_2026.md) — Full analysis of all sources
- [DATA_ENRICHMENT_SUMMARY.md](DATA_ENRICHMENT_SUMMARY.md) — Executive summary
- [CHANGELOG.md](CHANGELOG.md) — Evolution of our approach from initial estimates to Option 3

## Deployment

To deploy to GitHub Pages:

1. Create a new GitHub repository
2. Push the code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/sg-job-ai-impact.git
   git push -u origin main
   ```
3. Enable GitHub Pages:
   - Go to Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/docs`
   - Save and wait 1-2 minutes

Your site will be live at: `https://YOUR_USERNAME.github.io/sg-job-ai-impact/`

See [deploy-instructions.md](deploy-instructions.md) for detailed steps.

## Results

**Current Statistics (June 2026, Option 3)**:
- 441 occupations analyzed
- 2.38M total resident workforce
- ~110K workers (4.6%) with ★★★★★ registration data
- 1.51M PME workers (65.3%)
- Average AI exposure: 5.71/10 (job-weighted)
- PME AI exposure: 5.80/10

**Data Quality Evolution:**
- Initial (estimated): Absurd values (12K tram drivers, 50K gardeners)
- Option 1: 41 categories, 100% real but coarse
- Option 2: 441 categories, but unrealistic estimates
- **Option 3** ✓: 441 categories, registration anchors + multi-factor model, calibrated to MOM totals

## License

Data sources are from Singapore government agencies and are publicly available.

Code is provided as-is for educational purposes.
