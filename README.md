# Singapore Job Market AI Impact Visualizer

A Singapore version of [Andrej Karpathy's US Job Market Visualizer](https://karpathy.ai/jobs/), analyzing AI exposure across ~1,000 Singapore occupations using government data sources.

## Features

- **Comprehensive occupation coverage**: All ~1,002 SSOC 2024 occupations from SingStat
- **LLM-powered AI exposure scoring**: Uses Claude Opus 4.5 to rate each occupation's vulnerability to AI disruption (0-10 scale)
- **Real wage data**: Median salaries from MOM Occupational Wage Survey 2024
- **Employment estimates**: Distributed from MOM broad-group employment totals
- **Interactive treemap**: Visualize jobs by AI exposure, pay, education level, or major group
- **Singapore-specific insights**: PME exposure analysis and sector breakdowns

## Data Sources

1. **SSOC 2024** (Singapore Standard Occupational Classification) — occupation definitions and task descriptions
2. **MOM Occupational Wage Survey 2024** — median monthly wages by occupation
3. **data.gov.sg Employment Dataset** — employment counts by broad occupational group

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

### 4. Build employment weights
```bash
uv run python build_weights.py
```
Distributes broad employment totals to detailed occupations:
- `employment_weights.csv` — estimated employment per occupation

### 5. Score AI exposure (LLM)
```bash
uv run python score.py
```
**This is the longest step** (~1,000 API calls, ~5-10 minutes with rate limiting).
- Checkpoint after each occupation → `scores.json`
- Resumable if interrupted
- Cost estimate: ~$5 on GPT-4o

### 6. Build final site data
```bash
uv run python build_site_data.py
```
Merges all sources into:
- `site/data.json` — complete dataset for visualization

### 7. View the visualization
```bash
cd site
python -m http.server 8000
```
Open http://localhost:8000 in your browser.

## Known Limitations

⚠️ **Employment counts are estimates**: Singapore does not publish employment data at the 5-digit SSOC level. We distribute broad group totals proportionally across detailed occupations within each group. This is a modeling assumption, not ground truth.

⚠️ **Wage coverage**: MOM OWS covers ~500 occupations. The remaining ~500 will show pay: null.

⚠️ **No projections**: Unlike the US BLS, Singapore does not publish 10-year occupation growth projections, so we cannot include an "Outlook" layer.

⚠️ **AI exposure is subjective**: Scores reflect GPT-4o's assessment using the provided rubric, calibrated for Singapore's context. These are informed estimates, not predictions.

## Project Structure

```
.
├── fetch_data.py           # Download raw data sources
├── parse_ssoc.py           # Extract occupations from SSOC PDF
├── parse_wages.py          # Extract and match wage data
├── build_weights.py        # Estimate employment distribution
├── score.py                # LLM scoring pipeline
├── build_site_data.py      # Merge all data sources
├── raw/                    # Cached raw data (gitignored)
│   ├── ssoc2024.pdf
│   ├── mom_wages/*.xlsx
│   └── employment_by_occupation.json
├── occupations.json        # Parsed SSOC occupations
├── occupations.csv         # (Human-readable)
├── wages.csv               # Parsed wage data
├── employment_weights.csv  # Estimated employment
├── scores.json             # LLM AI exposure scores
└── site/
    ├── index.html          # Interactive visualization
    └── data.json           # Final merged dataset
```

## License

Data sources are from Singapore government agencies and are publicly available.

Code is provided as-is for educational purposes.
