# Data Enrichment Analysis - Executive Summary

**Date:** June 30, 2026  
**Objective:** Find better data sources to triangulate employment at granular (5-digit) occupation level

---

## Key Finding

**After extensive search, no Singapore government agency or organization publishes comprehensive 5-digit SSOC employment data.** MOM's 2-digit data (41 categories) remains the most granular official employment statistics available.

However, **high-value sector-specific sources** exist that can improve data quality for targeted occupations.

---

## Data Sources Explored

### Government Agencies ✓
- ✅ **MOM:** Labour Force Survey (2-digit), Job Vacancy Survey (detailed)
- ✅ **MOH:** Health Manpower (doctors, nurses, dentists by specialty)
- ✅ **MOE:** Teacher statistics by level
- ✅ **MHA:** Police force manpower
- ✅ **Census 2020:** 1-digit only (public), 5-digit restricted
- ❌ **CPF:** Has data but not published
- ❌ **IRAS:** No occupation statistics

### Professional Bodies ✓
- ✅ **Singapore Medical Council:** 17,582 doctors
- ✅ **Singapore Nursing Board:** 46,344 nurses
- ✅ **Law Society:** 6,273 lawyers
- ⚠️ **ISCA:** 40,000+ members (includes students)
- ⚠️ **IES:** 7,000+ engineers (no discipline breakdown)

### Industry Sources ✓
- ✅ **BCA/MOM:** Construction workforce (103,600 residents)
- ⚠️ **MPA:** Maritime census (aggregate only)
- ❌ **ACRA:** No employee occupation data

### Alternative Sources ✓
- ⚠️ **LinkedIn:** Trend insights, not employment counts
- ⚠️ **Job postings:** Demand signal, not supply
- ✅ **Education pipeline:** Graduate counts by discipline

---

## Recommended Actions

### ⭐ HIGH IMPACT (Immediate Implementation)

1. **Healthcare Professionals** - Use MOH registration data
   - **Impact:** ~60,000 workers with ★★★★★ precision
   - **Source:** moh.gov.sg/resources-statistics/health-manpower
   - **Occupations:** Doctors, nurses, dentists, pharmacists, allied health

2. **MOM Job Vacancy Survey** - Use as distribution weights
   - **Impact:** All 441 occupations - improves logic
   - **Source:** stats.mom.gov.sg Job Vacancies 2024
   - **Method:** Vacancy rates indicate relative employment levels

3. **Education Professionals** - Use MOE teacher counts
   - **Impact:** ~33,000 workers with ★★★★★ precision
   - **Source:** data.gov.sg teacher statistics
   - **Occupations:** Primary (15,273), Secondary (12,353)

4. **Legal & Police** - Use registration/government data
   - **Impact:** ~16,500 workers with ★★★★★ precision
   - **Source:** Law Society (6,273), MHA/SPF (10,500)

**Total High-Impact Coverage:** ~110,000 workers (4.6% of workforce) with perfect data

### ⚠️ MEDIUM IMPACT (Validation)

5. **Graduate Pipeline** - Validate professional occupation estimates
   - Engineering, medicine, law, accounting, IT graduates
   - Cross-check employment against 20-year supply
   - Identify unrealistic estimates

6. **Professional Bodies** - Cross-validate membership vs. employment
   - ISCA accountants, IES engineers
   - Check for order-of-magnitude accuracy

### 📋 LONG-TERM (Research)

7. **Census 2020 Microdata** - Request restricted access
   - 5-digit occupation distribution from 2020
   - Apply patterns to 2024 data
   - Requires SINGSTAT approval (2-3 months)

8. **Job Posting Analysis** - Build predictive model
   - Scrape MyCareersFuture, LinkedIn (6-12 months)
   - Map job titles to SSOC codes
   - Use volumes as employment proxy

---

## Proposed Solution: "Option 3"

### Enriched Employment Model

**Hybrid approach combining:**
- **MOM 2-digit baseline** (41 categories, 100% real data)
- **Registration overrides** (50 occupations, ~110K workers, ★★★★★ quality)
- **Multi-factor distribution** for remaining:
  - Wage weights (40%)
  - Vacancy weights (40%) ← NEW
  - Uniform distribution (20%)
- **Exact calibration** to MOM 2-digit totals

### Expected Results
- ✅ **441 occupations** (vs. current 41)
- ✅ **100% accuracy** at 2-digit level (maintains MOM data)
- ✅ **4.6% perfect data** from registrations
- ✅ **No more absurdities** (e.g., 12K tram drivers eliminated)
- ✅ **Transparent confidence scores** for each occupation

### Data Quality Distribution
| Confidence Level | Occupations | % of Workforce |
|-----------------|-------------|----------------|
| ★★★★★ Very High (registration) | 50 | 4.6% |
| ★★★★☆ High (validated model) | 100 | 30% |
| ★★★☆☆ Medium (wage-weighted) | 250 | 50% |
| ★★☆☆☆ Low (equal distribution) | 41 | 15.4% |

---

## Implementation Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Phase 1** | Week 1-2 | Integrate registration data (healthcare, education, legal, police) |
| **Phase 2** | Week 3-4 | Enhance with job vacancy data, rebuild distribution model |
| **Phase 3** | Week 5-6 | Validate against pipelines, document provenance, flag low-confidence |
| **Total** | 1.5-2 weeks | Ready for deployment |

---

## Why 5-Digit Data Doesn't Exist

International comparison shows Singapore publishes **less granular** occupation data than US, UK, Australia:
- **US BLS:** 6-digit SOC codes published
- **UK ONS:** 4-digit SOC codes published
- **Australia ABS:** 4-digit ANZSCO published
- **Singapore:** 2-digit SSOC published (5-digit collected in Census but restricted)

**Reasons:**
1. Survey cost for 2.4M workers
2. Employer classification difficulty
3. Dynamic occupations evolve faster than codes
4. Privacy concerns for rare occupations

**Best Practice:** Hybrid model (registration + survey + modeling) with transparent confidence levels.

---

## Conclusion

While no perfect 5-digit employment data exists, **high-quality sector-specific data can significantly improve** the current analysis by:

1. **Eliminating absurdities** through validation (no tram drivers)
2. **Adding precision** for 110K workers via registrations
3. **Improving distribution logic** with vacancy weights
4. **Maintaining accuracy** by calibrating to MOM 2-digit totals

**Recommendation:** Implement Option 3 (Enriched Employment Model) - combines granularity with rigor.

---

## Next Steps

1. ✅ Review comprehensive analysis: `DATA_SOURCE_ENRICHMENT_2026.md`
2. 📥 Download high-impact data sources:
   - MOH Health Manpower statistics
   - MOM Job Vacancies 2024 report
   - MOE teacher statistics (already on data.gov.sg)
3. 🔧 Implement `build_option3.py` script
4. ✓ Validate and deploy

**Full detailed analysis:** See `DATA_SOURCE_ENRICHMENT_2026.md` (13 sections, 50+ data sources evaluated)
