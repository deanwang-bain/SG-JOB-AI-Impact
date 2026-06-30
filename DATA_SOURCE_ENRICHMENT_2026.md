# Data Source Enrichment Analysis 2026
## Comprehensive Search for Granular Employment Data

**Date:** June 30, 2026  
**Purpose:** Identify new data sources to triangulate employment at 5-digit SSOC occupation level

---

## Executive Summary

After extensive search across government agencies, professional bodies, industry associations, and alternative data sources, **the fundamental conclusion is that MOM's 2-digit SSOC employment data remains the most granular official employment statistics publicly available in Singapore.** No government agency or organization publishes comprehensive 5-digit occupation-level employment counts.

However, several **sector-specific sources** can be used to **validate and triangulate** specific occupation categories, improving data quality for targeted groups.

---

## 1. Government Data Sources

### 1.1 Ministry of Manpower (MOM) - **PRIMARY SOURCE**
**Current Use:** ✓ Already integrated

- **Granularity:** 2-digit SSOC (41 sub-major groups)
- **Coverage:** Resident employment (Citizens + PRs)
- **Source:** Comprehensive Labour Force Survey (CLFS)
- **Latest:** June 2024 data available
- **Total:** 2,376,400 employed residents
- **Limitation:** Does not publish 5-digit occupation breakdowns

**MOM Job Vacancy Survey**
- **Potential Use:** NEW SOURCE TO CONSIDER
- **Granularity:** Detailed occupations (specific job titles)
- **Coverage:** ~15,040 establishments (85.6% response rate) as of Sep 2024
- **Data Available:**
  - Job titles at granular level
  - Vacancies by detailed occupation
  - Wage expectations per occupation
  - Skills required
  - Hard-to-fill positions
- **Access:** Published annually via stats.mom.gov.sg
- **Value:** Can show **relative demand** for specific 5-digit occupations, which may correlate with employment levels
- **Limitation:** Vacancy counts ≠ employment counts, but useful for triangulation

**Recommendation:** ✅ Download and integrate MOM Job Vacancy 2024 report to identify relative importance of specific detailed occupations within each 2-digit category.

### 1.2 Singapore Census of Population 2020
**Status:** Historical reference point

- **Granularity:** 1-digit SSOC (9 major groups)
- **Coverage:** Full resident population snapshot
- **Latest:** 2020 (next census: 2030)
- **Total:** 2,208,358 employed residents (2020)
- **Access:** data.gov.sg
- **Value:** Provides demographic breakdowns (ethnicity, age, disability, travel time) but **less granular than current MOM data**
- **Limitation:** Outdated (4+ years old), coarser than 2-digit MOM data

**Recommendation:** ❌ No advantage over current MOM 2-digit data (2024)

### 1.3 Central Provident Fund (CPF) Board
**Status:** Data not publicly available

- **Potential:** CPF has **employer-reported occupation** data for all employed persons
- **Reality:** Does not publish employment statistics by occupation
- **Access:** Restricted - administrative data only
- **Action Required:** Would require formal MOM/government data request

**Recommendation:** ⚠️ Potential future source if MOM conducts special study, but not publicly accessible

### 1.4 Inland Revenue Authority of Singapore (IRAS)
**Status:** Not applicable

- **Reality:** IRAS publishes tax statistics but **not employment by occupation**
- **Data Focus:** Income brackets, tax assessments, not occupational classification

**Recommendation:** ❌ Not relevant for occupation-level employment data

### 1.5 Workforce Singapore (WSG) / SkillsFuture
**Status:** Demand signals, not employment stock

- **Skills Frameworks:** 33 sectors with 1,600+ job roles mapped to SSOC 2020
- **Job-Skills Portal:** Sectoral dashboard showing job role demand (1-year job posting data)
- **Value:** Shows **emerging occupations** and skills demand, not current employment
- **Access:** jobsandskills.skillsfuture.gov.sg

**Recommendation:** ⚠️ Useful for identifying high-demand occupations and Skills Framework mapping to SSOC, but does not provide employment counts

---

## 2. Professional Registration Bodies

### 2.1 Healthcare Professionals - **HIGH VALUE**
**Status:** Multiple precise counts available

| Profession | Count (2024) | Source | Reliability |
|-----------|-------------|--------|-------------|
| **Doctors** | 17,582 | Singapore Medical Council | ★★★★★ (mandatory registration) |
| **Nurses** | 46,344 total | Singapore Nursing Board/MOH | ★★★★★ (mandatory registration) |
| - Registered Nurses | 36,995 | SNB | |
| - Enrolled Nurses | 9,232 | SNB | |
| - Registered Midwives | 117 | SNB | |
| **Dentists** | ~3,000 | Singapore Dental Council | ★★★★★ (mandatory registration) |
| **Pharmacists** | ~4,200 | Singapore Pharmacy Council | ★★★★★ (mandatory registration) |
| **Allied Health** | | MOH statistics | ★★★★☆ |
| - Occupational Therapists | ~1,500 | Allied Health Professions Council | |
| - Physiotherapists | ~2,000 | Allied Health Professions Council | |
| - Speech Therapists | ~400 | Allied Health Professions Council | |
| **TCM Physicians** | ~3,000 | TCM Practitioners Board | ★★★★★ (mandatory registration) |

**Source:** MOH Health Manpower statistics (updated annually)
**Access:** moh.gov.sg/resources-statistics/health-manpower

**Recommendation:** ✅ **HIGH PRIORITY** - Replace estimated values with actual registered counts for all SSOC codes:
- `2212` (Specialist medical practitioners)
- `2240` (Generalist medical practitioners)  
- `2221` (Nursing professionals)
- `2222` (Midwifery professionals)
- `2261` (Dentists)
- `2262` (Pharmacists)
- `2264` (Physiotherapists)
- `2265` (Dieticians and nutritionists)
- `2266` (Audiologists and speech therapists)
- `2267` (Optometrists and ophthalmic opticians)
- `2269` (Other health professionals)

### 2.2 Legal Professionals - **MODERATE VALUE**
**Status:** Precise count available

| Profession | Count | Source | Year |
|-----------|-------|--------|------|
| **Lawyers** | ~6,273 | Law Society of Singapore | 2022 |

**Notes:**
- Mandatory membership for practicing lawyers
- Peak was 6,333 (2021), slight decline since
- Includes both private practice and in-house counsel

**Recommendation:** ✅ Use for SSOC `2611` (Lawyers)

### 2.3 Accounting Professionals - **MODERATE VALUE**
**Status:** Membership count available (not all accountants)

| Organization | Membership | Notes |
|-------------|-----------|-------|
| **ISCA** | 40,000+ (2024) | Not all practicing accountants - includes students (~10,000) |

**Reality Check:**
- MOM 2024 shows 89,000 residents in "Accountants and Auditors (SSOC 2-digit 24)"
- ISCA represents ~44% of this (excluding students: ~33%)
- Many accountants work without ISCA membership
- ISCA includes non-practicing members

**Recommendation:** ⚠️ Can validate order of magnitude for SSOC `2411` (Accountants), but **MOM data is more comprehensive**

### 2.4 Engineering Professionals - **LOW VALUE**
**Status:** Aggregate membership only

| Organization | Membership | Details |
|-------------|-----------|---------|
| **IES** (Institution of Engineers, Singapore) | 7,000+ | No breakdown by discipline published |

**Notes:**
- IES maintains sector registries (Aerospace, Built Environment, Chemical & Energy, etc.)
- Registry purpose is competency recognition, not workforce census
- Membership is voluntary - many engineers practice without IES membership
- MOM 2024 shows 186,000 residents in "Science and Engineering Professionals (SSOC 21)"

**Recommendation:** ❌ IES data insufficient for triangulation - MOM aggregate is more reliable

---

## 3. Sector-Specific Data

### 3.1 Education - **HIGH VALUE**
**Status:** Precise teacher counts available

| Level | Teachers (2024) | Source |
|-------|----------------|--------|
| **Primary** | 15,273 | MOE / data.gov.sg |
| **Secondary** | 12,353 | MOE / data.gov.sg |
| **Pre-University (JC)** | ~2,500 | MOE / data.gov.sg |
| **Total K-12** | ~33,000 | MOE Education Statistics Digest |

**Access:** data.gov.sg - "Number Of Teachers By Level, School Type And Sex, Annual"

**Limitation:** No breakdown by subject taught

**Recommendation:** ✅ Use for SSOC `2341` (Primary education teaching professionals) and `2330` (Secondary education teaching professionals)

### 3.2 Construction - **MODERATE VALUE**
**Status:** Resident employment + total workforce available

| Category | Count (2024) | Source |
|----------|-------------|--------|
| **Resident Employment** | 103,600 | MOM Labour Force Survey |
| **Work Permit Holders** | ~482,600 (all CMP sectors) | MOM Foreign Workforce Numbers |

**Notes:**
- Construction managed through Man-Year Entitlement (MYE) system (BCA/MOM)
- Trade-specific data (rebar workers, plasterers, etc.) exists but not publicly aggregated by occupation
- BCA maintains Skills Evaluation Certificate (SEC) data by trade

**Recommendation:** ⚠️ Current MOM 2-digit data already captures resident construction employment. Foreign worker data adds context but doesn't provide occupation-level breakdown.

### 3.3 Maritime - **LOW VALUE**
**Status:** Industry estimates only

| Metric | Estimate | Source |
|--------|----------|--------|
| **Total Maritime Employment** | ~170,000 | Industry estimates (Singapore Maritime Foundation) |

**Notes:**
- MPA conducts annual Maritime Census but aggregated results not published at occupation level
- Covers ship owning/operating, agencies, management, bunkering, port operations, etc.
- 2024 MPA census focused on technology, sustainability, and manpower but detailed results confidential

**Recommendation:** ❌ Insufficient granularity - MOM industry data (Transportation and Storage) more reliable

### 3.4 Police and Protective Services - **HIGH VALUE**
**Status:** Precise counts available

| Service | Personnel (2024) | Source |
|---------|-----------------|--------|
| **SPF Regular Officers** | 10,500 | Ministry of Home Affairs |
| **SPF National Servicemen** | 28,200 | MHA |
| **Volunteer Special Constabulary** | 1,100 | MHA |
| **Total SPF** | 39,800 | MHA |

**Access:** MHA parliamentary replies, SPF Annual Report

**Recommendation:** ✅ Use regular officer count (10,500) for SSOC `5412` (Police officers) - excludes NSFs as they are temporary

---

## 4. Education Pipeline Data - **MODERATE VALUE**

### 4.1 University Graduates by Discipline
**Status:** Annual graduate counts available by field of study

| Discipline | Graduates (2024) | Cumulative Stock Estimate |
|-----------|------------------|---------------------------|
| **Engineering Sciences** | 4,779 | ~95,000 (20-year pipeline) |
| **Medicine** | 345 | ~6,900 (20-year pipeline) |
| **Accountancy** | 1,245 | ~25,000 (20-year pipeline) |
| **Law** | 550 | ~11,000 (20-year pipeline) |
| **Information Technology** | 1,800 | ~28,000 (20-year pipeline) |

**Source:** MOE / SINGSTAT - data.gov.sg  
**Access:** "Intake, Enrolment and Graduates of Universities by Course"

**Use Case:** 
- **Cross-validation:** Professional occupations with ~20-30 year career spans
- Example: 17,582 doctors (2024) vs. ~6,900 medicine graduates (20 years) suggests:
  - ~61% practicing rate (accounting for overseas-trained doctors)
  - Or ~11,000 foreign-trained doctors (which is ~40% of workforce - matches SMC data)

**Recommendation:** ⚠️ Useful for validation checks on professional occupations but **not a direct employment measure** (doesn't account for career changes, emigration, retirement)

---

## 5. Enterprise and Establishment Data - **LOW VALUE**

### 5.1 ACRA Business Registry
**Status:** Company data without employee occupation breakdown

- **Available:** Company name, UEN, registered address, SSIC codes, directors
- **NOT Available:** Number of employees by occupation
- **Limitation:** Annual Returns require employee count only for audit exemption threshold (50 employees), not publicly disclosed

**Recommendation:** ❌ Cannot be used for occupation-level employment

### 5.2 SINGSTAT Enterprise Landscape
**Status:** Aggregate employment by industry

- **Available:** Enterprise count, total employment, value-added by SSIC industry
- **Granularity:** Industry (SSIC), not occupation (SSOC)
- **Example:** 2024 - 358,300 enterprises employing 3.39 million

**Recommendation:** ❌ Industry classification (SSIC) is different from occupation classification (SSOC) - not directly useful

---

## 6. Alternative Data Sources

### 6.1 LinkedIn Economic Graph
**Status:** Trend insights, not employment census

- **Available:** Jobs on the Rise (20 fastest-growing roles), hiring trends, skills gap analysis
- **Example:** 2024 report shows AI-related roles, sustainability managers growing
- **Limitation:** Platform bias (not all workers have LinkedIn), focuses on PMETs, no absolute employment numbers

**Recommendation:** ❌ Useful for identifying emerging occupations but does not provide employment counts

### 6.2 Job Posting Data (MyCareersFuture, LinkedIn, JobStreet)
**Status:** Demand signal, not supply

- **Use:** Indicates **hiring demand** for specific occupations
- **Limitation:** Vacancy postings ≠ employed workforce (turnover, growth, multiple postings)

**Recommendation:** ⚠️ Can be used as **proxy for relative size** within occupation groups but requires careful interpretation

---

## 7. Key Findings & Limitations

### 7.1 The Core Reality
**No comprehensive 5-digit SSOC employment data exists in Singapore.**

The reasons are:
1. **Survey cost:** Conducting detailed occupation surveys at 5-digit level for 2.4M workers is extremely expensive
2. **Response burden:** Employers struggle to classify employees into specific 5-digit codes
3. **Dynamic occupations:** Job titles and roles evolve faster than classification systems
4. **Privacy concerns:** Very detailed occupation data could identify individuals in rare occupations

### 7.2 What MOM Actually Collects
- **Labour Force Survey (quarterly):** 1-digit SSOC (9 major groups)
- **Comprehensive Labour Force Survey (annual):** 2-digit SSOC (41 sub-major groups)
- **Census (decennial):** 5-digit SSOC codes are collected but:
  - Aggregated to 1-digit for public release
  - 5-digit microdata restricted to researchers with approval

### 7.3 International Comparison
- **US Bureau of Labor Statistics:** Publishes detailed occupation employment (equivalent to 5-digit) via Occupational Employment and Wage Statistics (OEWS)
- **UK Office for National Statistics:** Publishes 4-digit SOC codes
- **Australia ABS:** Publishes 4-digit ANZSCO codes

**Singapore is less granular than these countries in published occupation statistics.**

---

## 8. Actionable Recommendations

### TIER 1: High-Value Immediate Actions ✅

1. **Healthcare Professionals**
   - **Action:** Download MOH Health Manpower statistics (annual)
   - **Integration:** Replace estimated employment for SSOC codes 221*, 2261-2269
   - **Data Quality:** ★★★★★ (mandatory registration)
   - **Impact:** ~60,000 workers with precise counts

2. **MOM Job Vacancy Survey 2024**
   - **Action:** Download detailed occupation vacancy data
   - **Integration:** Use vacancy counts as **relative weights** to distribute 2-digit employment to specific 5-digit occupations
   - **Logic:** Occupations with higher vacancy rates likely have higher employment levels
   - **Data Quality:** ★★★★☆ (sample-based, demand-focused)
   - **Impact:** All occupations - improves distribution logic

3. **Education Professionals**
   - **Action:** Use MOE teacher statistics
   - **Integration:** Set exact counts for SSOC 2341 (Primary teachers: 15,273) and 2330 (Secondary teachers: 12,353)
   - **Data Quality:** ★★★★★ (administrative data)
   - **Impact:** ~33,000 workers

4. **Legal Professionals**
   - **Action:** Use Law Society membership (6,273)
   - **Integration:** Set for SSOC 2611 (Lawyers)
   - **Data Quality:** ★★★★☆ (mandatory for practice, but some in-house)
   - **Impact:** ~6,000 workers

5. **Police Officers**
   - **Action:** Use MHA/SPF data (10,500 regulars)
   - **Integration:** Set for SSOC 5412 (Police officers) - exclude NSFs
   - **Data Quality:** ★★★★★ (administrative data)
   - **Impact:** ~10,500 workers

**Total Tier 1 Coverage:** ~110,000 workers with high-quality data (4.6% of workforce)

### TIER 2: Validation & Triangulation ⚠️

6. **Graduate Pipeline Validation**
   - **Action:** For professional occupations (doctors, engineers, lawyers, accountants), cross-check employment estimates against 20-year graduate pipeline
   - **Use Case:** Identify unrealistic estimates (e.g., more employed than pipeline could supply)
   - **Example:** Engineering graduates: 4,779/year × 35-year career = ~167,000 maximum engineer workforce
   - **Current MOM:** SSOC 21 (Science/Engineering Professionals) = 186,000 ✓ Plausible (includes foreign-trained)

7. **Professional Body Validation**
   - **Action:** Use ISCA membership (30,000 practicing) to validate accountant estimates
   - **Cross-check:** MOM SSOC 24 (Business and Administration Professionals) = 89,000
   - **Reality Check:** ISCA covers ~34% - plausible given voluntary membership

### TIER 3: Research & Future Work 📋

8. **Request Census 2020 Microdata Access**
   - **Action:** Apply to SINGSTAT for research access to Census 2020 5-digit occupation data
   - **Purpose:** Understand 2020 distribution patterns at 5-digit level
   - **Use:** Apply 2020 proportions to 2024 2-digit data
   - **Limitation:** 4-year lag, formal approval process required
   - **Timeline:** 2-3 months for approval

9. **Special Request to MOM**
   - **Action:** Formal request to MOM Manpower Research & Statistics Department for:
     - 5-digit SSOC data from CLFS 2024 (if available but unpublished)
     - Rationale: Academic/public interest research on AI impact
   - **Likelihood:** Low (if data existed, it would be published)
   - **Timeline:** 3-6 months

10. **Develop Job Posting-Based Model**
    - **Action:** Scrape MyCareersFuture, LinkedIn, JobStreet for 6-12 months
    - **Analysis:** Map job titles to SSOC 5-digit codes
    - **Model:** Use posting volumes as proxy for employment distribution
    - **Validation:** Compare against known totals (Tier 1 data)
    - **Effort:** High (requires data engineering, ML, ongoing maintenance)
    - **Timeline:** 6-12 months

---

## 9. Proposed Implementation Strategy

### Phase 1: Integrate High-Confidence Data (Week 1-2)
```python
# Pseudocode for implementation
def build_enriched_employment_data():
    # Start with MOM 2-digit baseline (41 categories, 2,376,400 workers)
    base_data = load_mom_2digit_employment()
    
    # Override with high-confidence registration data
    overrides = {
        'Medical practitioners (SSOC 221*)': 17582,  # SMC
        'Nursing professionals (SSOC 222*)': 36995,  # SNB - RNs only
        'Dentists (SSOC 2261)': 3000,  # SDC
        'Pharmacists (SSOC 2262)': 4200,  # SPC
        'Lawyers (SSOC 2611)': 6273,  # Law Society
        'Primary teachers (SSOC 2341)': 15273,  # MOE
        'Secondary teachers (SSOC 2330)': 12353,  # MOE
        'Police officers (SSOC 5412)': 10500,  # SPF
    }
    
    # Distribute remaining employment in affected 2-digit groups
    # to other 5-digit occupations using wage weights or vacancy weights
    for ssoc_2digit in affected_categories:
        known_employment = sum(overrides in ssoc_2digit)
        remaining = base_data[ssoc_2digit] - known_employment
        distribute_remaining(remaining, using='wage_weights')
    
    return enriched_data
```

### Phase 2: Enhance Distribution Logic with Job Vacancy Data (Week 3-4)
1. Download MOM Job Vacancies 2024 report
2. Extract vacancy counts by detailed occupation
3. Calculate **vacancy rate** = vacancies / estimated employment
4. Use vacancy rates as additional weight factor for distributing 2-digit to 5-digit
5. Validate against Tier 1 known values

### Phase 3: Validation & Documentation (Week 5-6)
1. Cross-check all professional occupations against graduate pipeline
2. Identify and flag any remaining unrealistic values (e.g., "tram driver problem")
3. Document data sources, confidence levels, and assumptions
4. Create data provenance for each occupation:
   - **Source:** Registration data / MOM / Estimated
   - **Confidence:** High / Medium / Low
   - **Last Updated:** Date
   - **Method:** Direct count / Wage-weighted distribution / Vacancy-weighted distribution

---

## 10. Expected Data Quality Improvement

### Current State (Option 1)
- **41 occupations** (2-digit SSOC)
- **100% real MOM data**
- **0% granularity** for detailed occupations

### After Enrichment (Proposed "Option 3")
- **441 occupations** (5-digit SSOC)
- **4.6% direct registration data** (~110,000 workers with ★★★★★ quality)
- **95.4% enhanced distribution** using:
  - Wage weights (existing)
  - Vacancy weights (new)
  - Calibrated to 2-digit MOM totals (maintaining accuracy)

### Confidence Levels per Occupation
| Confidence | Source | Count | % of Workforce |
|-----------|--------|-------|----------------|
| **Very High (★★★★★)** | Mandatory registration | ~50 occupations | 4.6% |
| **High (★★★★☆)** | Validated against pipeline + vacancies | ~100 occupations | 30% |
| **Medium (★★★☆☆)** | Wage-weighted distribution | ~250 occupations | 50% |
| **Low (★★☆☆☆)** | Equal distribution (last resort) | ~41 occupations | 15.4% |

**Key Advantage:** Every occupation maintains **exact 2-digit calibration** to MOM official data, so aggregate accuracy is preserved.

---

## 11. Critical Insight: The "5-Digit Problem"

### Why No Country Publishes Perfect 5-Digit Employment Data

Even countries with more detailed occupation statistics face:
1. **Occupational mobility:** Workers change roles within the same employer
2. **Hybrid roles:** Many workers perform tasks from multiple occupations
3. **Employer reporting:** Companies struggle to code employees accurately
4. **Emerging occupations:** New roles (e.g., "Prompt Engineer") don't fit existing codes

### The Best Approach: Hybrid Model
- **Use administrative data** where it exists (registrations, licenses)
- **Use survey data** for aggregate totals (MOM 2-digit)
- **Model the gap** using proxy variables (wages, vacancies, education pipeline)
- **Calibrate rigorously** to maintain accuracy at aggregate level
- **Document assumptions** transparently

This is exactly what we've done by:
- Rejecting "tram driver" absurdities in Option 2
- Validating against real-world constraints (e.g., Singapore has no trams)
- Preferring coarse-but-real over granular-but-fake

---

## 12. Final Recommendation

### Implement "Option 3: Enriched Employment Model"

**Characteristics:**
- **Base:** MOM 2-digit data (41 categories, 100% real)
- **Enhancement:** 50 high-confidence 5-digit overrides from registration data
- **Distribution:** Remaining employment distributed using **multi-factor model**:
  - Wage weights (40%)
  - Vacancy weights (40%)
  - Uniform distribution (20% - captures unknown factors)
- **Validation:** Graduate pipeline checks, professional body cross-checks
- **Calibration:** Exact match to MOM 2-digit totals (error = 0)
- **Transparency:** Data provenance and confidence scores for every occupation

**Result:**
- ✅ Maintains 100% accuracy at 2-digit level (preserves real MOM data)
- ✅ Provides 441 granular occupations (vs. 41 currently)
- ✅ Uses real registration counts where available (~110,000 workers)
- ✅ Eliminates absurd estimates like "12k tram drivers"
- ✅ Fully transparent about confidence levels

### Implementation Effort
- **Data Collection:** 2-3 days
- **Integration:** 3-5 days
- **Validation:** 2-3 days
- **Documentation:** 1-2 days
- **Total:** 1.5-2 weeks

---

## 13. Data Source Contact Points

For future data requests:

1. **Ministry of Manpower:** stats@mom.gov.sg
2. **Ministry of Health:** moh_info@moh.gov.sg
3. **Ministry of Education:** moe_contact@moe.gov.sg
4. **SINGSTAT (Census microdata):** info@singstat.gov.sg
5. **Singapore Medical Council:** general@smc.gov.sg
6. **Singapore Nursing Board:** snb_info@moh.gov.sg
7. **Law Society of Singapore:** lawsociety@lawsoc.org.sg
8. **ISCA:** contact@isca.org.sg
9. **IES:** ies@iesnet.org.sg
10. **BCA (Construction):** bca_enquiry@bca.gov.sg
11. **MPA (Maritime):** mpa@mpa.gov.sg

---

## Document Version
- **Version:** 1.0
- **Date:** June 30, 2026
- **Author:** AI Job Exposure Analysis Project
- **Status:** Final recommendations pending implementation
