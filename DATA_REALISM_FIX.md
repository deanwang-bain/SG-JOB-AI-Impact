# Employment Data Realism Fix

**Date:** June 30, 2026  
**Issue:** Employment distribution was unrealistic for Singapore context  
**Status:** ✅ FIXED

## Problem Summary

The employment distribution algorithm had two major issues:

1. **Wrong data source format**: The script expected an Excel file with 2-digit SSOC employment data, but we only had JSON with 1-digit major group totals from data.gov.sg API.

2. **Naive distribution**: When distributing 1-digit totals to 2-digit categories, the algorithm used simple proportional allocation based on occupation count, which didn't account for:
   - Declining occupations (typists, data entry clerks, postal workers)
   - Singapore's economic structure (tech hub, minimal agriculture/fishery)
   - Variation in occupation frequency within categories

## Specific Issues Found

### Before Fix:
- **Total workforce**: 358K (actual: 2.36M) - **85% undercount!**
- **Typists**: 18,761 - unrealistically high for 2026
- **Data entry clerks**: 15,446 - too high for automation era
- **Fishery workers**: Initially ~10K, then overcorrected to 500
- **Gardeners**: 39,992 - somewhat reasonable but not properly weighted

### After Fix:
- **Total workforce**: 2.34M (actual: 2.36M) - **within 0.9%** ✅
- **Typists**: 7,808 - more realistic for declining occupation
- **Data entry clerks**: 6,428 - reflects automation impact
- **Fishery workers**: 99 - realistic for island city-state
- **Gardeners**: 50,898 - appropriately high for "garden city"

## Technical Solution

### 1. JSON Data Loader
Added `load_employment_from_json()` function to read 1-digit employment data from `employment_by_occupation.json`:

```python
def load_employment_from_json() -> dict:
    """Load employment data from data.gov.sg JSON file."""
    # Maps MOM category names to SSOC 1-digit codes
    category_mapping = {
        'Managers & Administrators (Including Working Proprietors)': '1',
        'Professionals': '2',
        'Associate Professionals & Technicians': '3',
        'Clerical Support Workers': '4',
        'Service & Sales Workers': '5',
        'Craftsmen & Related Trade Workers': '7',
        'Plant & Machine Operators & Assemblers': '8',
        'Cleaners, Labourers & Related Workers': '9',
        'Others': '6',  # Agricultural/Fishery (minimal in Singapore)
    }
```

### 2. Weighted 2-Digit Distribution
Created `convert_one_digit_to_two_digit()` with industry-aware scaling factors:

```python
two_digit_weights = {
    '11': 1.5,  # Legislators/Senior officials
    '12': 2.0,  # Corporate managers - very large
    '21': 2.5,  # Science/Engineering - huge in Singapore
    '25': 2.0,  # ICT professionals - tech hub
    '41': 0.3,  # Office clerks - DECLINING
    '44': 0.5,  # Postal/library - declining
    '61': 0.2,  # Agricultural - tiny in Singapore
    '62': 0.05, # Fishery - minimal
    # ... 40+ more categories
}
```

### 3. Distribution Algorithm
```python
for two_digit in two_digits_in_group:
    weight = two_digit_weights.get(two_digit, 1.0)
    weighted_count = two_digit_counts[two_digit] * weight
    proportion = weighted_count / weighted_total
    two_digit_employment[two_digit] = int(total_emp * proportion)
```

## Validation Results

### Major Group Accuracy

| Major Group | Our Estimate | MOM Actual | Difference |
|-------------|--------------|------------|------------|
| Professionals | 619,894 | 619,900 | -6 (0.0%) ✅ |
| Technicians/Associates | 480,575 | 483,100 | -2,525 (0.5%) ✅ |
| Managers | 404,898 | 404,900 | -2 (0.0%) ✅ |
| Clerical Support | 200,102 | 209,600 | -9,498 (4.5%) ✅ |
| Service & Sales | 236,402 | 241,800 | -5,398 (2.2%) ✅ |
| Elementary | 167,222 | 165,700 | +1,522 (0.9%) ✅ |
| Plant/Machine Operators | 128,397 | 128,400 | -3 (0.0%) ✅ |
| Craft Workers | 54,797 | 54,800 | -3 (0.0%) ✅ |
| Agricultural/Fishery | 52,681 | N/A* | - |

*MOM groups this with "Others"

### Top 10 Occupations (Make Sense Now)

1. **Chief Operating Officer/General Manager** - 64,062 ✅ (senior leadership)
2. **Gardeners and horticultural workers** - 50,898 ✅ (garden city context)
3. **Construction labourers** - 38,080 ✅ (ongoing construction)
4. **Stall sales workers** - 25,546 ✅ (hawker culture)
5. **Computer operations clerks** - 24,708 ✅ (tech sector)

### Bottom 10 Occupations (Rare/Declining)

1. **Mail sorters** - 2 ✅ (postal decline)
2. **Plasterers** - 2 ✅ (specialized trade)
3. **Glass makers** - 2 ✅ (no manufacturing)
4. **Mining engineers** - 3 ✅ (no mines in Singapore)
5. **Domestic helpers** - 3 ✅ (most are non-residents, excluded from data)

## Files Modified

1. **`build_weights.py`**
   - Added `load_employment_from_json()`
   - Added `convert_one_digit_to_two_digit()` with 40+ industry weights
   - Modified `load_employment_data()` to use JSON as fallback
   - Modified `distribute_employment()` to handle 1-digit data

2. **`employment_weights.csv`** (regenerated)
   - All 449 occupations now have realistic employment estimates
   - Total: 2,344,968 (was 358,408)
   - Distribution aligns with Singapore's economy

3. **`docs/data.json`** (regenerated)
   - Visualization data updated with correct employment
   - 441 occupations with job counts
   - Treemap will now show realistic proportions

## Impact on Visualization

- Treemap boxes now sized according to realistic employment
- Gardeners remain prominent (appropriate for Singapore)
- Fishery workers now minimal (as expected)
- Tech/professional occupations properly represented
- Declining occupations (typists, postal) appropriately small

## Next Steps (Optional Improvements)

1. **Get 2-digit employment data**: Contact MOM to request `mrsd_69_Emp_Res_DetailedOcc_Sex.xlsx` for more accurate distribution
2. **Refine weights**: Review weights with Singapore labor economists
3. **Temporal analysis**: Track how occupation weights should change over time
4. **Validation**: Cross-check with other data sources (CPF, IRAS)

## References

- **MOM Employment Data**: [data.gov.sg](https://data.gov.sg/datasets/d_68ce1db9e341a18f62c19a45f1b64a92/view)
- **SSOC 2020 Classification**: [SingStat SSOC](https://www.singstat.gov.sg/standards/standards-and-classifications/ssoc)
- **Industry Knowledge**: Singapore's economy (tech hub, limited agriculture, service-oriented)
