# Data Source Recommendations for Singapore Job Market AI Impact Visualizer

**Generated:** 2026-06-30  
**Current Data Version:** 2026-03-26  
**Analysis Scope:** 432 occupations, 2.27M workers

---

## Executive Summary

This document identifies data gaps in the current analysis and proposes additional data sources to enhance the Singapore Job Market AI Impact Visualizer. The analysis currently has **46.5% wage coverage**, uses **estimated employment distributions**, and lacks **temporal trends** and **non-resident workforce data**.

### Critical Findings

1. 🔴 **Raw data sources are missing** — `raw/` directory not populated
2. ⚠️ **Upstream SSOC 2024 PDFs return 404** — source URLs may have changed
3. ⚠️ **Data is 3 months old** (March 2026) — consider quarterly refresh
4. ⚠️ **Low wage coverage** — 201/432 occupations (46.5%)
5. ⚠️ **No projections** — Singapore doesn't publish 10-year occupation outlooks like US BLS

---

## 1. Immediate Actions (Next 7 Days)

### 1.1 Refresh Existing Data Sources

**Priority:** 🔴 CRITICAL

**Action Items:**
- [ ] Re-run `fetch_data.py` to update cached raw data
- [ ] Verify SSOC 2024 PDF URL (currently returns 404)
- [ ] Check for MOM Occupational Wage Survey 2025 or mid-2026 updates
- [ ] Update employment statistics with latest data.gov.sg releases

**Expected Impact:**
- Resolve missing raw data files
- Update to June 2026 employment data if available
- Capture any new wage survey releases

**Implementation:**
```bash
# Verify URLs first
curl -I "https://www.singstat.gov.sg/-/media/files/standards_and_classifications/occupational_classification/ssoc2024report.ashx"

# Run data fetch
uv run python fetch_data.py

# Re-run full pipeline
uv run python parse_ssoc.py
uv run python parse_wages.py
uv run python build_weights.py
uv run python score.py  # Only if SSOC occupations changed
uv run python build_site_data.py
```

---

## 2. Fill Wage Coverage Gap (Currently 46.5%)

### 2.1 SkillsFuture Singapore (SSG) Salary Guide

**Source:** https://www.skillsfuture.gov.sg/  
**Coverage:** Industry-specific salary benchmarks for ~150-200 roles  
**Update Frequency:** Annual  
**Priority:** 🟡 HIGH

**What It Provides:**
- Industry-specific salary ranges (25th, 50th, 75th percentile)
- Education level requirements
- Years of experience tiers
- Cross-industry comparisons

**How to Integrate:**
1. Scrape or download SSG salary guide (if publicly available)
2. Map SSG job titles to SSOC 2024 codes using fuzzy matching
3. Use as supplementary wage data for occupations not covered by MOM
4. Priority: Focus on roles with high AI exposure scores but no wage data

**Expected Improvement:** +15-25% wage coverage → **60-70% total**

**Code Changes Required:**
- New script: `fetch_ssg_wages.py`
- Update `parse_wages.py` to merge SSG data with MOM data
- Add data source attribution in site metadata

---

### 2.2 JobsBank Singapore Historical Postings

**Source:** https://www.mycareersfuture.gov.sg/api  
**Coverage:** Real-time job postings with salary ranges  
**Update Frequency:** Daily  
**Priority:** 🟡 HIGH

**What It Provides:**
- Actual salary ranges from job postings (~80,000+ active listings)
- Occupation titles and descriptions
- Skills requirements
- Industry and company size distribution

**How to Integrate:**
1. Query MyCareersFuture API for bulk job posting data
2. Extract salary ranges for each occupation title
3. Map to SSOC 2024 codes using NLP (GPT-4 or Claude for mapping)
4. Calculate median/mean salary from posting ranges
5. Use as fallback for occupations without MOM wage data

**Expected Improvement:** +30-40% wage coverage → **75-85% total**

**Caveats:**
- Salary ranges may be inflated (posted vs. actual)
- Job titles may not map cleanly to SSOC codes
- API access may require approval

**Code Changes Required:**
- New script: `fetch_jobsbank_wages.py`
- Add salary range normalization (convert ranges to point estimates)
- Add confidence scoring based on sample size

---

### 2.3 LinkedIn Salary Insights

**Source:** LinkedIn Salary Tool (https://www.linkedin.com/salary/)  
**Coverage:** Self-reported salaries from LinkedIn members  
**Update Frequency:** Real-time  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Singapore-specific salary data by job title
- Years of experience breakdown
- Company size and industry filters
- Total compensation (base + bonus + equity)

**How to Integrate:**
1. Manual data collection (no public API)
2. Focus on high-visibility, high-AI-exposure roles
3. Use for validation and gap-filling

**Expected Improvement:** +10-15% wage coverage → **55-60% total**

**Caveats:**
- Requires manual scraping or premium access
- Self-reported data may have reporting bias
- Terms of service may restrict automated collection

---

### 2.4 Public Sector Salary Guidelines

**Source:** Public Service Division (PSD) and Statutory Board Salary Disclosures  
**Coverage:** Civil service and statutory board positions  
**Update Frequency:** Annual  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Salary ranges for public sector occupations
- Clear job grade structures (e.g., EDB, MAS, MOE salary scales)
- Transparent progression pathways

**How to Integrate:**
1. Compile public sector salary scales from official disclosures
2. Map to SSOC codes (e.g., "Teacher" → 23300, "Policy Officer" → 24210)
3. Use as reference for government-related occupations

**Expected Improvement:** +5-10% wage coverage → **51-55% total**

**Sources:**
- PSD Singapore: https://www.psd.gov.sg/
- Statutory boards' annual reports and career pages
- Parliamentary salary disclosures for senior roles

---

## 3. Improve Employment Data Accuracy

### 3.1 Request Detailed Employment Data from MOM

**Source:** Ministry of Manpower (direct request)  
**Coverage:** 5-digit SSOC occupation-level employment counts  
**Priority:** 🔴 CRITICAL (if available)

**Current Gap:**
- Analysis uses 41 sub-major groups (2-digit SSOC)
- Distribution to 432 occupations (5-digit) is **estimated** using statistical modeling

**What to Request:**
- Resident employment by 5-digit SSOC code (if available)
- Non-resident employment breakdown by occupation
- Quarterly employment trends (2023-2026)

**How to Integrate:**
1. Email MOM Statistics Division (mom_statistics@mom.gov.sg)
2. Request: "Detailed employment statistics by 5-digit SSOC 2024 occupation codes"
3. If available, replace `build_weights.py` with actual counts

**Expected Improvement:**
- Eliminate estimation uncertainty
- Provide **actual** occupation-level employment counts
- Enable more accurate AI exposure impact calculations

**Alternative:**
- If 5-digit data unavailable, request 4-digit data for better granularity

---

### 3.2 Census of Population 2020/2025 Occupation Data

**Source:** SingStat Census of Population  
**Coverage:** Detailed occupation breakdown every 10 years  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Full population-level occupation data
- Cross-tabulations with age, education, industry
- Historical trends (2010, 2020, 2030 projections if available)

**How to Integrate:**
1. Download Census 2020 detailed occupation tables from SingStat
2. Check if Census 2025 data available (expected mid-2026)
3. Use as validation for MOM employment estimates

**Expected Improvement:**
- Validate employment distribution model
- Identify under-represented occupations
- Benchmark against historical trends

**Source URL:** https://www.singstat.gov.sg/publications/reference/cop2020

---

### 3.3 Non-Resident Workforce Data

**Source:** MOM Foreign Workforce Numbers  
**Coverage:** Work permit, S Pass, Employment Pass holders  
**Priority:** 🟡 HIGH

**Current Gap:**
- Analysis only covers 2.27M resident workers
- Excludes ~1M non-resident workers (~30% of total workforce)

**What It Provides:**
- Employment Pass holders by industry and occupation
- S Pass and Work Permit holders by sector
- Temporal trends (monthly/quarterly)

**How to Integrate:**
1. Fetch MOM foreign workforce statistics from data.gov.sg
2. Map to SSOC occupation codes (challenging due to coarser categories)
3. Add as separate dataset or merge with resident employment
4. Create non-resident AI exposure analysis

**Expected Improvement:**
- Comprehensive workforce coverage (100% vs. current 70%)
- Identify occupations heavily reliant on non-residents
- Policy-relevant insights on work pass exposure to AI

**Source URLs:**
- https://stats.mom.gov.sg/Pages/Foreign-Workforce-Summary.aspx
- https://data.gov.sg (search "foreign workforce numbers")

---

## 4. Add Temporal Dimension (Historical Trends)

### 4.1 Historical MOM Employment Data (2015-2026)

**Source:** MOM Labour Market Statistics Archive  
**Coverage:** 2-digit SSOC employment back to 2015+  
**Priority:** 🟡 HIGH

**What It Provides:**
- 10+ years of employment trends by occupation
- Identify growing vs. declining occupations
- Correlate with technology adoption waves

**How to Integrate:**
1. Download historical employment datasets from MOM/data.gov.sg
2. Normalize to SSOC 2024 codes (handle SSOC 2010 → 2020 → 2024 mapping)
3. Add "Employment Trend (5Y)" field to visualization
4. Enable time-series analysis layer

**Expected Improvement:**
- Show historical growth/decline rates
- Identify accelerating or decelerating trends
- Contextualize AI impact within broader automation trends

**Visualization Enhancements:**
- Add "Trend" color mode (growing vs. declining)
- Show sparklines for each occupation
- Enable time-slider for historical comparison

---

### 4.2 Quarterly Employment Updates (2023-2026)

**Source:** MOM Labour Market Reports (quarterly)  
**Coverage:** Latest 3-year quarterly data  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Recent employment fluctuations
- COVID-19 recovery patterns
- Emerging occupation shifts

**How to Integrate:**
1. Set up automated quarterly data refresh pipeline
2. Update employment weights every quarter
3. Track quarter-over-quarter changes

**Expected Improvement:**
- Keep analysis current (reduce lag time)
- Capture recent AI-driven shifts
- Enable "freshness" indicator on site

---

## 5. Add Skills and Tasks Data

### 5.1 O*NET Skills and Tasks Database (Adapted for Singapore)

**Source:** O*NET Online (https://www.onetonline.org/)  
**Coverage:** ~1,000 occupations with detailed skills/tasks  
**Priority:** 🟡 HIGH

**What It Provides:**
- Detailed task descriptions (100-200 tasks per occupation)
- Skills taxonomy (35+ skills with importance/level ratings)
- Work activities, work context, and tools used
- Automation potential scores (from academic research)

**How to Integrate:**
1. Download O*NET database (free API or bulk download)
2. Map US SOC codes to Singapore SSOC codes (manual or LLM-assisted)
3. Adapt task descriptions for Singapore context (e.g., "CPA" → "CA Singapore")
4. Use task data to validate/refine AI exposure scores

**Expected Improvement:**
- More granular AI exposure scoring
- Task-level automation predictions
- Enable "similar occupations" feature based on task overlap

**Alternative:** Skills Future Framework (SSG)
- Singapore-specific skills taxonomy
- Industry-specific skills mapping
- May require collaboration with SSG

---

### 5.2 Singapore Workforce Skills Qualifications (WSQ)

**Source:** SkillsFuture Singapore  
**Coverage:** ~1,000+ WSQ courses mapped to occupations  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Skills required for each occupation
- Training pathways and certification levels
- Industry-validated competency standards

**How to Integrate:**
1. Scrape WSQ course catalog and skills frameworks
2. Map WSQ skills to SSOC occupation codes
3. Use for "reskilling pathways" recommendations

**Expected Improvement:**
- Show required skills for transitioning between occupations
- Highlight upskilling opportunities for high-AI-exposure roles
- Link to SkillsFuture courses

---

## 6. Add Education and Certification Data

### 6.1 University Employment Surveys

**Source:** NUS, NTU, SMU, SIT, SUTD Graduate Employment Surveys  
**Coverage:** Fresh graduate employment outcomes  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Starting salaries by degree and occupation
- Employment rates by field of study
- Industry placement patterns

**How to Integrate:**
1. Compile graduate employment data from university annual reports
2. Map degree programs to entry-level SSOC occupations
3. Add "Education Level" filter and "Starting Salary" data

**Expected Improvement:**
- Show career entry points by degree
- Highlight AI-exposed occupations popular among graduates
- Policy insights for education planning

---

### 6.2 Professional Certifications Registry

**Source:** Professional boards (e.g., ISCA for accountants, SMA for doctors)  
**Coverage:** Licensed professionals by occupation  
**Priority:** 🟢 LOW

**What It Provides:**
- Number of licensed professionals by specialty
- Certification requirements and renewal rates
- Demographic breakdowns (age, gender)

**How to Integrate:**
1. Compile certification data from professional boards
2. Use for occupations requiring licensure (doctors, lawyers, engineers, accountants)
3. Validate employment estimates for regulated professions

---

## 7. Add Industry and Sector Context

### 7.1 SSIC Industry Classification Mapping

**Source:** Singapore Standard Industrial Classification (SSIC)  
**Coverage:** Map occupations to industries  
**Priority:** 🟡 HIGH

**What It Provides:**
- Link occupations to industries (e.g., "Software Developer" in Finance vs. Tech)
- Industry-specific AI adoption rates
- Sectoral employment distribution

**How to Integrate:**
1. Create SSOC ↔ SSIC mapping table
2. Add industry data to each occupation
3. Enable "Industry" filter in visualization

**Expected Improvement:**
- Show AI exposure by industry sector
- Identify industries most impacted by AI
- Enable industry-specific policy analysis

---

### 7.2 Economic Development Board (EDB) Industry Reports

**Source:** EDB Singapore Annual Reports and Industry Insights  
**Coverage:** Strategic industries and growth sectors  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Industry-specific AI adoption trends
- Government investment priorities
- Emerging sectors (e.g., biotech, green tech)

**How to Integrate:**
1. Review EDB reports for AI adoption by industry
2. Add "Strategic Priority" flag to relevant occupations
3. Contextualize AI exposure within government strategy

---

## 8. Add AI Technology Adoption Data

### 8.1 Enterprise AI Adoption Surveys

**Source:** IDC, Gartner, or Singapore Computer Society surveys  
**Coverage:** Enterprise AI adoption rates by industry/function  
**Priority:** 🟡 HIGH

**What It Provides:**
- Which industries are adopting AI fastest
- Which functions (HR, Finance, Sales) are automating
- Budget allocations for AI investments

**How to Integrate:**
1. Purchase or obtain industry reports (may require licensing)
2. Map adoption rates to occupation categories
3. Add "Adoption Speed" dimension to visualization

**Expected Improvement:**
- Show which occupations face near-term vs. long-term AI impact
- Identify early vs. late-stage automation sectors
- Inform urgency of reskilling initiatives

---

### 8.2 Singapore AI Research Papers and Studies

**Source:** AI Singapore, SUTD, NUS AI research  
**Coverage:** Academic assessments of AI impact on Singapore workforce  
**Priority:** 🟢 MEDIUM

**What It Provides:**
- Singapore-specific AI exposure research
- Validation of LLM-generated scores
- Task-level automation probabilities

**How to Integrate:**
1. Literature review of Singapore AI workforce studies (2020-2026)
2. Compare published AI exposure scores with GPT-4o scores
3. Use as validation dataset and citation source

**Example Studies:**
- "The Future of Work in Singapore" (various authors)
- SkillsFuture AI impact assessments
- NTUC or MOM commissioned studies

---

## 9. Add International Comparisons

### 9.1 US Bureau of Labor Statistics (BLS) Data

**Source:** https://www.bls.gov/oes/ (Occupational Employment and Wage Statistics)  
**Coverage:** US occupation data for comparison  
**Priority:** 🟢 LOW

**What It Provides:**
- 10-year occupation outlook projections
- Detailed task descriptions (via O*NET)
- Comparative wage levels

**How to Integrate:**
1. Download BLS occupation data
2. Map US SOC codes to Singapore SSOC codes
3. Add "US Comparison" view (salaries, growth rates)

**Expected Improvement:**
- Benchmark Singapore wages vs. US
- Highlight occupations with growth divergence
- Inform talent attraction/retention strategies

---

### 9.2 OECD Employment Database

**Source:** https://stats.oecd.org/  
**Coverage:** International occupation and skills data  
**Priority:** 🟢 LOW

**What It Provides:**
- Cross-country employment patterns
- International skill taxonomies
- Automation risk assessments (Frey & Osborne, Arntz et al.)

**How to Integrate:**
1. Download OECD occupation statistics
2. Map ISCO codes to SSOC codes
3. Add international context layer

---

## 10. Improve Data Infrastructure

### 10.1 Set Up Automated Data Pipeline

**Priority:** 🔴 CRITICAL

**Implementation:**
1. Create GitHub Actions workflow for quarterly data refresh
2. Set up monitoring for upstream data source changes
3. Add automated testing for data quality
4. Implement alerting for broken data sources

**Code Changes:**
```yaml
# .github/workflows/data-refresh.yml
name: Quarterly Data Refresh
on:
  schedule:
    - cron: '0 0 1 */3 *'  # 1st day of every 3rd month
  workflow_dispatch:  # Manual trigger

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Fetch data
        run: uv run python fetch_data.py
      - name: Test data freshness
        run: uv run python test_data_freshness.py
      - name: Create issue if data stale
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Data refresh failed - action required',
              body: 'Automated data refresh encountered issues. Check workflow logs.'
            })
```

---

### 10.2 Add Data Version Control

**Priority:** 🟡 HIGH

**Implementation:**
1. Use DVC (Data Version Control) for large data files
2. Track data provenance and lineage
3. Enable rollback to previous data versions

**Code Changes:**
```bash
# Install DVC
pip install dvc

# Initialize DVC
dvc init

# Track data files
dvc add raw/ occupations.json wages.csv employment_weights.csv scores.json

# Commit to git
git add .dvc .gitignore occupations.json.dvc
git commit -m "Add data versioning"

# Set up remote storage (e.g., S3, Google Cloud Storage)
dvc remote add -d myremote s3://mybucket/dvc-storage
dvc push
```

---

### 10.3 Create Data Quality Dashboard

**Priority:** 🟢 MEDIUM

**Implementation:**
1. Build monitoring dashboard showing:
   - Data freshness (days since last update)
   - Coverage metrics (wage, employment, scores)
   - Data quality indicators (completeness, consistency)
   - Upstream source status (green/yellow/red)

**Tool Options:**
- Streamlit dashboard (Python)
- Observable notebook (JavaScript)
- Tableau/Power BI (if enterprise)

---

## 11. Address Known Data Issues

### 11.1 Fix SSOC 2024 PDF URL (Returns 404)

**Priority:** 🔴 CRITICAL

**Action:**
1. Check SingStat website for updated URL
2. Contact SingStat to report broken link
3. Add URL fallback mechanism (try SSOC 2020 if 2024 unavailable)

**Possible Updated URLs:**
- Check: https://www.singstat.gov.sg/standards/standards-and-classifications/ssoc
- Alternative: Request PDF directly from SingStat Statistics Division

---

### 11.2 Improve Wage Fuzzy Matching

**Priority:** 🟡 HIGH

**Current Issue:**
- Only 201/432 occupations matched (46.5%)
- Fuzzy matching threshold may be too strict

**Improvements:**
1. Lower similarity threshold from 60% to 50%
2. Add manual mapping file for difficult cases
3. Use LLM (GPT-4) to suggest mappings for unmatched occupations
4. Add occupation title synonyms dictionary

**Code Changes:**
- Update `parse_wages.py` matching logic
- Add `manual_wage_mappings.csv` for edge cases
- Implement LLM-assisted mapping with human review

---

### 11.3 Add Data Quality Indicators

**Priority:** 🟢 MEDIUM

**Implementation:**
1. Add confidence scores to each data point
2. Flag estimated vs. actual employment counts
3. Show wage data source (MOM vs. estimated)
4. Add "Last Updated" timestamp per field

**Visualization Changes:**
- Add tooltip showing data quality
- Color-code by confidence level
- Show "Data last updated: YYYY-MM-DD" on hover

---

## 12. Summary of Recommendations

### Priority Matrix

| Data Source | Impact | Effort | Priority | Expected Improvement |
|------------|--------|--------|----------|---------------------|
| Refresh existing data | High | Low | 🔴 CRITICAL | Fix missing raw data |
| JobsBank API wages | High | Medium | 🟡 HIGH | +30-40% wage coverage |
| MOM 5-digit employment | High | Low | 🔴 CRITICAL | Eliminate employment estimates |
| Non-resident workforce | High | Medium | 🟡 HIGH | +30% workforce coverage |
| Historical employment | Medium | Medium | 🟡 HIGH | Add temporal trends |
| O*NET skills data | Medium | High | 🟡 HIGH | Task-level AI exposure |
| SSG salary guide | Medium | Low | 🟡 HIGH | +15-25% wage coverage |
| SSIC industry mapping | Medium | Low | 🟡 HIGH | Enable industry analysis |
| Automated pipeline | Medium | Medium | 🔴 CRITICAL | Ensure data freshness |
| AI adoption surveys | Medium | High | 🟡 HIGH | Validate AI impact timeline |
| LinkedIn salaries | Low | High | 🟢 MEDIUM | +10-15% wage coverage |
| University employment | Low | Medium | 🟢 MEDIUM | Entry-level insights |
| International comparisons | Low | Medium | 🟢 LOW | Benchmarking context |

---

### Implementation Roadmap

#### Phase 1 (Next 2 Weeks)
1. ✅ Re-fetch existing data sources
2. ✅ Fix SSOC 2024 URL issue
3. ✅ Set up automated data freshness testing
4. ✅ Request MOM 5-digit employment data

#### Phase 2 (Next 1-2 Months)
1. Integrate JobsBank API for wage data
2. Add non-resident workforce data
3. Improve wage fuzzy matching (target 70% coverage)
4. Set up automated quarterly refresh pipeline

#### Phase 3 (Next 3-6 Months)
1. Add historical employment trends (2015-2026)
2. Integrate O*NET skills data
3. Add SSIC industry classification mapping
4. Create data quality dashboard

#### Phase 4 (6+ Months)
1. Add AI adoption survey data
2. Build reskilling pathways recommendations
3. International comparisons layer
4. Publish data API for researchers

---

## Appendix A: Data Source Contact Information

| Organization | Contact | Purpose |
|-------------|---------|---------|
| Ministry of Manpower | mom_statistics@mom.gov.sg | Employment data, wage surveys |
| SingStat | info@singstat.gov.sg | SSOC classifications, Census data |
| SkillsFuture Singapore | enquiry@ssg.gov.sg | Skills frameworks, WSQ data |
| Data.gov.sg | feedback@data.gov.sg | API access, data requests |
| Economic Development Board | edb@edb.gov.sg | Industry insights |

---

## Appendix B: Data Licensing and Attribution

Ensure compliance with data licensing terms:

1. **MOM Data:** Attributed as per terms of use
2. **SingStat Data:** Singapore Open Data License
3. **O*NET:** Public domain (US Department of Labor)
4. **LinkedIn/JobsBank:** Check Terms of Service before scraping
5. **Academic Research:** Cite appropriately

Add comprehensive attribution page to visualization site.

---

## Appendix C: Estimated Costs

| Data Source | Cost | Frequency |
|------------|------|-----------|
| MOM/SingStat data | Free | Quarterly |
| JobsBank API | Free (with approval) | Monthly |
| O*NET database | Free | Annual |
| IDC/Gartner reports | $500-2000/report | Annual |
| LLM API (re-scoring) | $2-5 | Per update |
| Cloud storage (DVC) | $5-20/month | Ongoing |

**Total Annual Cost:** ~$100-500 (excluding premium industry reports)

---

**Document Prepared By:** Data Freshness Analysis Tool  
**Recommended Review Frequency:** Quarterly  
**Next Review Date:** 2026-09-30
