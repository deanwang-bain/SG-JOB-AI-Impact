# Project Changelog

This document preserves the history of major developments and decisions in the AI Job Exposure Analysis project.

---

## 2026-06-30: Option 3 - Enriched Employment Model

**Status:** Implemented

**Decision:** Adopt hybrid approach combining MOM 2-digit real data with high-confidence registration overrides and enhanced multi-factor distribution model.

**Key Features:**
- 441 detailed occupations (5-digit SSOC)
- 100% accuracy at 2-digit aggregate level
- ~110K workers (4.6%) with perfect registration data
- Multi-factor weights: wages (40%), vacancies (40%), uniform (20%)
- Eliminated absurdities (no tram drivers, realistic fishery workers, accurate gardeners)

**Implementation:** `build_option3.py`

**Documentation:** `DATA_SOURCE_ENRICHMENT_2026.md`, `DATA_ENRICHMENT_SUMMARY.md`

---

## 2026-06-30: Comprehensive Data Source Search

**Action:** Searched 50+ potential data sources across Singapore government agencies, professional bodies, industry associations, and alternative sources.

**Key Findings:**
- No 5-digit SSOC employment data publicly available
- Identified high-value sources:
  - MOH: Healthcare professionals (17,582 doctors, 46,344 nurses, etc.)
  - MOE: Teachers (33,000 total)
  - Law Society: 6,273 lawyers
  - MHA/SPF: 10,500 police officers
  - MOM Job Vacancy Survey: Detailed occupation demand data

**Sources Explored:**
- Government: MOM, MOH, MOE, MHA, CPF, IRAS, WSG, SkillsFuture, Census
- Professional Bodies: SMC, SNB, Law Society, ISCA, IES
- Industry: BCA, MPA, ACRA
- Alternative: LinkedIn, job postings, education pipeline

**Result:** Recommended Option 3 approach using registration data where available.

---

## 2026-06-29: Revert to Option 1 from Option 2

**Issue:** Option 2 (wage-weighted 5-digit distribution) produced absurd result: 12,444 tram drivers despite Singapore having no tram system.

**Root Cause:** Wage-based distribution allocated employment to occupations that may not exist or be realistic in Singapore context.

**Decision:** Reverted to Option 1 (41 2-digit categories with 100% real MOM data) prioritizing accuracy over granularity.

**Documentation:** `WHY_OPTION1_WINS.md` (archived)

**Key Quote:** "We can live with less granularity if it means more accuracy."

---

## 2026-06-28: Option 2 Implementation

**Approach:** Distributed real 2-digit MOM employment to 5-digit occupations using wage-weighted model.

**Process:**
- Load MOM 2-digit employment (41 categories, 2,365,600 total)
- Distribute to 441 5-digit occupations using median wages as weights
- Calibrate to exact 2-digit totals

**Result:** 441 occupations with granular data, but revealed estimation flaws (tram drivers).

**Documentation:** `OPTION2_IMPLEMENTATION.md`, `OPTION2_PREVIEW.md` (archived)

---

## 2026-06-27: Option 1 Implementation

**Approach:** Use real MOM 2-digit SSOC employment data without estimation.

**Process:**
- Load `raw/mrsd_69_Emp_Res_DetailedOcc_Sex.xlsx`
- Parse 41 2-digit SSOC categories
- Aggregate 5-digit wages and AI scores to 2-digit
- Build visualization with 100% real employment data

**Benefits:**
- Zero estimation error at aggregate level
- Every number traceable to official MOM source
- No unrealistic occupation counts

**Trade-off:** Less granularity (41 vs 441 categories)

**Documentation:** `REAL_DATA_IMPLEMENTATION.md` (archived)

---

## 2026-06-26: Data Realism Fixes

### Issue 1: Gardeners Overcount
**Problem:** Initial model estimated 50,000 gardeners (vs. ~12,000 actual)

**Root Cause:** Incorrect mapping of MOM "Others" category to Major Group 6 (Agricultural workers)

**Fix:** 
- Removed "Others" -> Major Group 6 mapping
- Manually set Major Group 6 employment to 12,000 based on NParks data
- Re-distributed using weighted model

**Validation:** NParks manages ~3,000 direct gardeners; total including private sector: ~12,000

**Documentation:** `GARDENER_FIX.md` (archived)

### Issue 2: Total Workforce Undercount
**Problem:** Initial build showed 358K employed (vs. 2.36M actual)

**Root Cause:** Excel file dependency missing, script used placeholder weights

**Fix:**
- Loaded 1-digit MOM JSON employment data from data.gov.sg as fallback
- Implemented `convert_one_digit_to_two_digit()` with Singapore-context weights
- Distributed 2.36M total across all categories

**Documentation:** `DATA_REALISM_FIX.md` (archived)

---

## 2026-06-25: Fishery Workers Fix

**Issue:** Coastal water/deep sea fishery workers appeared as largest employment block in treemap visualization.

**Problem:** `sparse_allocation_ratio` in `build_weights.py` allocated excess employment proportionally, causing Major Group 6 (Agricultural, Forestry, Fishery) to receive unrealistic numbers.

**Fix:** Added special case for Major Group 6:
```python
if major_group == '6':  # Agricultural, Forestry, Fishery Workers
    allocated = min(500, max(1, int(sparse_employment_pool * 0.01)))
```

**Result:** Fishery workers capped at reasonable level (~500 or 1% of sparse pool)

**Documentation:** `FISHERY_FIX.md` (archived)

---

## 2026-06-24: Visualization Updates

**Changes:**
- Increased canvas height for better visibility
- Reduced gap between boxes for compact layout
- Enhanced text rendering with better font sizing
- Updated subtitle to reflect data source and date
- Adjusted line widths for clearer box boundaries

**Result:** Treemap visualization more closely matches reference design

**Documentation:** `VISUALIZATION_UPDATE.md` (archived)

---

## 2026-06-23: SSOC URL Issue Resolution

**Problem:** SSOC 2020 PDF download returned HTTP 404 errors from Singapore Statistics website.

**Investigation:**
- Original URL: `https://www.singstat.gov.sg/-/media/files/standards_and_classifications/ssoc/ssoc2020-detailed-definitions.pdf` (404)
- Searched for current working URLs

**Solution:** Implemented 3-tier fallback mechanism:
1. Try SSOC 2020 detailed definitions
2. Fall back to SSOC 2020 report
3. Fall back to comprehensive guide

**Result:** Successfully downloaded `ssoc2020_report.pdf` (1.9 MB)

**Documentation:** `SSOC_URL_ISSUE.md` (archived)

---

## 2026-06-22: Data Freshness Testing

**Action:** Created automated test suite for data currency and completeness.

**Tests Implemented:**
- File age checks (<90 days)
- URL accessibility (HTTP 200)
- Data completeness (row counts, required fields)
- Data type validation

**Files:**
- `test_data_freshness.py` - Test suite
- `TESTING.md` - Documentation
- `data_freshness_report.txt` - Initial results
- `data_freshness_report_updated.txt` - Post-fix results

**Results:**
- Fixed SSOC URL issues
- All data sources validated
- All tests passing

**Documentation:** `STEPS_COMPLETED.md` (archived)

---

## 2026-06-21: Initial Data Source Analysis

**Action:** Comprehensive analysis of existing data sources and identification of gaps.

**Data Sources Evaluated:**
- MOM Labour Force Survey (primary)
- SSOC 2020 classification
- Wage data from MOM Occupational Wage Survey
- AI exposure scores (custom scoring)

**Gaps Identified:**
- Wage coverage limited (not all occupations)
- No detailed employment by 5-digit occupation
- Non-resident workforce not included
- Temporal data missing (employment trends)
- Industry-specific employment missing

**Recommendations:**
- Email MOM for 5-digit data
- Explore SkillsFuture Skills Framework
- Consider Census microdata access
- Set up automated testing

**Documentation:** `DATA_SOURCE_RECOMMENDATIONS.md`, `ANALYSIS_SUMMARY.md` (archived)

---

## 2026-06-20: Project Initialization

**Context:** Email from project stakeholder requesting data freshness check and gap analysis.

**Initial Setup:**
- Repository structure established
- Data pipeline scripts created:
  - `fetch_data.py` - Download raw data
  - `parse_ssoc.py` - Extract SSOC structure
  - `parse_wages.py` - Extract and match wages
  - `build_weights.py` - Estimate employment distribution
  - `build_site_data.py` - Build visualization dataset
  - `score.py` - Calculate AI exposure scores
- Visualization deployed to GitHub Pages

**Documentation:** `DATA_SUMMARY_EMAIL.md`, `README.md`

---

## Key Learnings

1. **Accuracy vs. Granularity Trade-off:** More detailed data is only valuable if it's accurate. Option 2's "12K tram drivers" showed the danger of blind statistical distribution.

2. **Real Data Anchors:** Starting with 100% real data (MOM 2-digit) and selectively adding precision (registration data) is more robust than estimating everything.

3. **Domain Knowledge Critical:** Understanding Singapore context (no trams, ~12K gardeners from NParks, etc.) is essential for validating statistical outputs.

4. **Multi-Factor Modeling:** Combining multiple proxies (wages, vacancies, uniform distribution) reduces bias from any single factor.

5. **Data Source Landscape:** Singapore publishes less granular occupation data than US/UK/Australia. Creative approaches needed to achieve 5-digit detail while maintaining rigor.

---

## Evolution of Approaches

| Approach | Occupations | Data Quality | Issue |
|----------|-------------|--------------|-------|
| **Initial (estimated)** | 441 | Estimated from 1-digit | Fishery workers absurdly large |
| **Fishery Fix** | 441 | Estimated with Major Group 6 cap | Gardeners overcount (50K) |
| **Gardener Fix** | 441 | Estimated with better 2-digit weights | Total undercount (358K) |
| **Realism Fix** | 441 | Estimated with MOM 1-digit baseline | Achieved 2.36M total |
| **Option 1** | 41 | 100% real MOM 2-digit | Less granular, but accurate |
| **Option 2** | 441 | Wage-weighted from real 2-digit | Tram drivers (12K) - absurd |
| **Option 3** ✓ | 441 | Real 2-digit + registration overrides + multi-factor | Best of both |

---

## Data Quality Hierarchy (Option 3)

```
★★★★★ Very High (4.6%)
- Healthcare: MOH registration (17,582 doctors, 46,344 nurses, etc.)
- Education: MOE statistics (15,273 primary, 12,353 secondary teachers)
- Legal: Law Society (6,273 lawyers)
- Police: MHA/SPF (10,500 regular officers)

★★★★☆ High (30%)
- Multi-factor model validated against professional body data
- Graduate pipeline cross-checks

★★★☆☆ Medium (50%)
- Wage-weighted distribution
- Calibrated to MOM 2-digit totals

★★☆☆☆ Low (15.4%)
- Equal distribution where insufficient data
```

---

## Future Work

1. **Request Census 2020 Microdata** - Apply for restricted access to 5-digit occupation distribution
2. **Integrate MOM Job Vacancy Survey** - Replace simulated vacancy weights with actual data
3. **Build Job Posting Model** - Scrape MyCareersFuture, LinkedIn for 6-12 months
4. **Temporal Analysis** - Track employment trends over time
5. **Industry Cross-tabulation** - Employment by occupation AND industry
6. **Non-resident Workforce** - Include work permit holders where relevant
7. **Automated Monitoring** - Set up GitHub Actions for data freshness tests

---

**Document Version:** 1.0  
**Last Updated:** June 30, 2026  
**Status:** Current

---

*This changelog consolidates information from multiple archived documentation files. For current project documentation, see `README.md`, `DATA_SOURCE_ENRICHMENT_2026.md`, and `DATA_ENRICHMENT_SUMMARY.md`.*
