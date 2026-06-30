# Data Freshness Testing Guide

This guide explains how to use the automated data freshness testing tools to ensure your Singapore Job Market AI Impact Visualizer data is current and complete.

## Quick Start

Run the data freshness test:

```bash
python3 test_data_freshness.py
```

The script will check:
- ✅ Existence and age of all data files
- ✅ Accessibility of upstream data sources
- ✅ Data completeness metrics
- ✅ Currency of data (last updated dates)

## Understanding the Report

The test generates a comprehensive report with four levels of information:

### 🔴 Critical Issues
**Action Required Immediately**

These indicate data problems that will significantly impact analysis quality:
- Missing essential data files
- Extremely outdated data (>2 years)
- Broken upstream data sources
- Data integrity problems

**Example:**
```
🔴 CRITICAL ISSUES (Action Required):
  • SSOC 2024 PDF is MISSING: raw/ssoc2024.pdf
  • Employment Data API is MISSING: raw/employment_by_occupation.json
```

**What to do:** Run `uv run python fetch_data.py` immediately to refresh data.

---

### ⚠️ Issues Found
**Refresh Recommended**

These indicate data that should be refreshed soon:
- Data files older than recommended age threshold
- Moderate data quality concerns
- Incomplete coverage metrics

**Example:**
```
⚠️  ISSUES FOUND:
  • SSOC 2024 PDF is 400 days old (threshold: 730 days)
  • Wage coverage low: 201/432 occupations (46.5%)
```

**What to do:** Schedule a data refresh within the next 1-2 weeks.

---

### ⚡ Warnings
**Monitor These Issues**

These are informational warnings that don't require immediate action:
- Upstream URL changes
- Non-critical data source timeouts
- Minor data quality observations

**Example:**
```
⚡ WARNINGS:
  • SSOC 2020 PDF (fallback) URL returned HTTP 404
  • Employment data is from 2024, more recent data may be available
```

**What to do:** Note for next scheduled refresh, check for URL updates.

---

### ✓ Information
**Current Status**

These show the current state of your data:
- File sizes and last modified dates
- Data completeness metrics
- Successful URL checks
- Summary statistics

**Example:**
```
✓ INFORMATION:
  • Occupations: 433 total
  • Wage coverage: 201/432 occupations (46.5%)
  • Total employment: 2,265,744 workers
  • Site data generated: 2026-03-26
```

**What to do:** Review for context, no action needed.

---

## Exit Codes

The script uses exit codes for automation/CI integration:

| Exit Code | Status | Meaning | Action |
|-----------|--------|---------|--------|
| `0` | ✅ Success | Data is current, no issues found | None |
| `1` | 🔴 Critical | Critical issues found, immediate action required | Run `fetch_data.py` now |
| `2` | ⚠️ Warning | Refresh recommended | Schedule data refresh |

### Using in CI/CD

```bash
# Run test and capture exit code
python3 test_data_freshness.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ]; then
    echo "Critical data issues found!"
    exit 1
elif [ $EXIT_CODE -eq 2 ]; then
    echo "Data refresh recommended"
    # Optionally trigger refresh workflow
fi
```

---

## Understanding Metrics

### Wage Coverage
```
Wage coverage: 201/432 occupations (46.5%)
```

**What it means:** Only 46.5% of SSOC occupations have matched wage data from MOM surveys.

**Why it matters:** Low coverage means many occupations will show "pay: null" in the visualization.

**How to improve:** See `DATA_SOURCE_RECOMMENDATIONS.md` for strategies to increase coverage to 75-85%.

---

### Employment Distribution
```
Employment weights: 433 occupations
Total employment: 2,265,744 workers
```

**What it means:** Employment has been distributed from 41 sub-major groups (2-digit SSOC) to 433 detailed occupations (5-digit).

**Why it matters:** These are **estimates**, not actual occupation-level counts. The total (2.27M) matches official MOM data, but individual occupation splits use statistical modeling.

**How to improve:** Request actual 5-digit employment data from MOM (see recommendations).

---

### AI Exposure Scores
```
AI exposure scores: 432 occupations scored
```

**What it means:** All occupations have been scored for AI exposure using GPT-4o.

**Why it matters:** Complete scoring enables full analysis. Incomplete scoring would show gaps in visualization.

**How to improve:** If <100%, re-run `score.py` to complete scoring.

---

### Data Age Thresholds

The test uses these thresholds to determine if data needs refresh:

| Data Source | Max Age | Rationale |
|-------------|---------|-----------|
| SSOC PDF | 730 days (2 years) | SSOC updates infrequently (2010 → 2020 → 2024) |
| MOM Wages | 365 days (1 year) | Annual Occupational Wage Survey |
| Employment Data | 365 days (1 year) | Annual employment statistics |

---

## Common Issues and Solutions

### Issue: "Raw data files are MISSING"

**Explanation:** The `raw/` directory is gitignored and not committed to the repository. This is expected.

**Solution:**
```bash
uv run python fetch_data.py
```

This downloads:
- SSOC 2024 PDF from SingStat
- MOM wage survey Excel files
- Employment data from data.gov.sg

---

### Issue: "SSOC 2024 PDF URL returned HTTP 404"

**Explanation:** The upstream URL may have changed or the file may have been moved.

**Solution:**
1. Visit https://www.singstat.gov.sg/standards/standards-and-classifications/ssoc
2. Find the current SSOC 2024 report URL
3. Update `SSOC_2024_URL` in `fetch_data.py`
4. Re-run fetch

**Alternative:** The script will fall back to SSOC 2020 if SSOC 2024 is unavailable.

---

### Issue: "Wage coverage low (46.5%)"

**Explanation:** MOM wage surveys don't cover all SSOC occupations, and fuzzy title matching has limitations.

**Solution (Short-term):**
1. Lower fuzzy matching threshold in `parse_wages.py` (60% → 50%)
2. Add manual mapping file for difficult cases
3. Re-run pipeline

**Solution (Long-term):**
See `DATA_SOURCE_RECOMMENDATIONS.md` for strategies to add:
- JobsBank API data (+30-40% coverage)
- SkillsFuture salary guide (+15-25%)
- LinkedIn salary insights (+10-15%)

---

### Issue: "Employment data is from 2024, more recent data may be available"

**Explanation:** The test detected that data is from a previous year.

**Solution:**
1. Check data.gov.sg for updated employment dataset
2. Check MOM Labour Market Reports for latest quarter
3. Update `EMPLOYMENT_RESOURCE_ID` in `fetch_data.py` if dataset changed
4. Re-run fetch

---

## Automated Monitoring

### Set Up Quarterly Checks

Add to your `crontab`:

```bash
# Run on 1st of every 3rd month (Jan, Apr, Jul, Oct)
0 0 1 */3 * cd /path/to/project && python3 test_data_freshness.py && mail -s "Data Freshness Report" you@example.com < data_freshness_report.txt
```

### GitHub Actions Workflow

Create `.github/workflows/data-freshness.yml`:

```yaml
name: Data Freshness Check

on:
  schedule:
    - cron: '0 0 1 */3 *'  # Quarterly
  workflow_dispatch:  # Manual trigger

jobs:
  test-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install httpx beautifulsoup4
      
      - name: Run data freshness test
        id: test
        run: |
          python3 test_data_freshness.py
          echo "exit_code=$?" >> $GITHUB_OUTPUT
        continue-on-error: true
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: data-freshness-report
          path: data_freshness_report.txt
      
      - name: Create issue if critical
        if: steps.test.outputs.exit_code == '1'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🔴 Critical: Data refresh required',
              body: 'Automated data freshness check found critical issues. See workflow artifacts for full report.',
              labels: ['data', 'critical']
            })
```

---

## Interpreting URL Check Results

The test attempts to verify that upstream data sources are still accessible:

### ✅ URL is accessible (HTTP 200)
Data source is available and responding normally.

### ⚠️ URL returned HTTP 404
The URL may have changed or the file may have been moved. Check the source website for updates.

### ⚠️ URL timed out
The data source didn't respond within 10 seconds. This could be temporary (network issues) or indicate the source is down.

### ⚠️ URL check failed: [error message]
Connection error, SSL certificate issue, or other technical problem. May require investigation.

---

## Data Quality Indicators

The test performs several data quality checks:

### Occupation Count Validation
```
Occupations: 433 total
```

**Expected:** ~432-433 occupations (SSOC 2024 standard)  
**Warning if:** <400 occupations (incomplete SSOC parsing)

### Employment Total Validation
```
Total employment: 2,265,744 workers
```

**Expected:** 2.0M - 2.5M workers (Singapore resident workforce)  
**Warning if:** Outside expected range (data quality issue)

### Scoring Completeness
```
AI exposure scores: 432 occupations scored
```

**Expected:** All 432 occupations scored  
**Warning if:** <432 (incomplete LLM scoring)

---

## Manual Data Inspection

After running the test, you can manually inspect files:

### Check raw data exists
```bash
ls -lh raw/
ls -lh raw/mom_wages/
```

### Check processed data timestamps
```bash
ls -lh *.{json,csv}
stat docs/data.json
```

### View wage coverage details
```bash
# Count occupations with wages
grep -v '^ssoc_code,title,median_monthly_wage' wages.csv | wc -l

# Sample wage data
head -20 wages.csv
```

### Check employment distribution
```bash
# View employment by major group
awk -F',' 'NR>1 {sum[$3]+=$5} END {for (g in sum) print g, sum[g]}' employment_weights.csv | sort -n
```

---

## Troubleshooting

### Test fails with import errors

**Error:** `ModuleNotFoundError: No module named 'httpx'`

**Solution:**
```bash
pip install httpx beautifulsoup4
# or
uv pip install httpx beautifulsoup4
```

---

### Test hangs during URL checks

**Explanation:** Network requests may timeout if upstream sources are slow or down.

**Solution:**
- Wait for timeout (default: 30 seconds)
- Or press Ctrl+C and review partial results
- Adjust `TIMEOUT` in script if needed

---

### Wrong Python version

**Error:** `SyntaxError: invalid syntax` (walrus operator, f-strings, etc.)

**Solution:**
```bash
python3 --version  # Should be 3.10+
python3 test_data_freshness.py
```

---

## Related Documentation

- **[DATA_SOURCE_RECOMMENDATIONS.md](DATA_SOURCE_RECOMMENDATIONS.md)** - Comprehensive guide to improving data coverage and quality
- **[README.md](README.md)** - Main project documentation
- **[deploy-instructions.md](deploy-instructions.md)** - Deployment guide

---

## Contributing

If you identify additional data quality checks that should be added to the test:

1. Open an issue describing the check
2. Or submit a PR with the enhancement
3. Include rationale for threshold values

---

**Last Updated:** 2026-06-30  
**Script Version:** 1.0  
**Maintained By:** Project maintainers
