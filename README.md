# Singapore Job Market AI Impact Visualizer

A Singapore version of [Andrej Karpathy's US Job Market Visualizer](https://karpathy.ai/jobs/), analyzing AI exposure across 432 Singapore occupations using government data sources.

**🌐 Live Demo**: [Your GitHub Pages URL will be here]

## Features

- **Comprehensive occupation coverage**: 432 detailed SSOC 2024 occupations
- **LLM-powered AI exposure scoring**: Uses OpenAI GPT-4o to rate each occupation's AI exposure (0-10 scale)
- **Employment data**: 2.31M workers distributed from MOM 2-digit SSOC employment data (2024)
- **Interactive treemap**: Visualize jobs by AI exposure, pay, education level, or major group
- **Adjustable view**: Slider to show top 10-432 jobs by employment
- **Singapore-specific insights**: PME exposure analysis (65.2% of workforce)

## Data Sources

1. **SSOC 2024** (Singapore Standard Occupational Classification) — occupation definitions and task descriptions from Ministry of Manpower
2. **MOM Detailed Employment Data 2024** — resident employment by 2-digit occupation codes (41 sub-major groups)
3. **MOM Occupational Wage Survey 2024** — median monthly wages for 201 occupations (46.5% coverage)
4. **OpenAI GPT-4o** — AI exposure scoring calibrated for Singapore context

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

## Known Limitations

⚠️ **Employment counts are estimates**: While based on MOM's 41 sub-major groups (2-digit SSOC), distribution to 432 detailed occupations (5-digit) uses statistical modeling with wage-weighted or random variation. Not actual occupation-level counts.

⚠️ **Partial wage coverage**: 201 of 432 occupations (46.5%) have wage data. Remaining occupations show pay: null in visualization.

⚠️ **No projections**: Unlike the US BLS, Singapore does not publish 10-year occupation growth projections, so we cannot include an "Outlook" layer.

⚠️ **Resident workers only**: Data covers ~2.31M resident workers (citizens and PRs), excluding non-resident workforce (~30% of total).

⚠️ **AI exposure is subjective**: Scores reflect GPT-4o's assessment using the provided rubric, calibrated for Singapore's context. These are informed estimates, not empirical measurements.

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
└── docs/
    ├── index.html          # Interactive visualization
    └── data.json           # Final merged dataset
```

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

**Current Statistics (March 2026)**:
- 432 occupations scored
- 2.31M total workforce
- 1.51M PME workers (65.3%)
- 201 occupations with wage data (46.5%)
- Average AI exposure: 5.71/10 (job-weighted)
- PME AI exposure: 5.80/10

## License

Data sources are from Singapore government agencies and are publicly available.

Code is provided as-is for educational purposes.
