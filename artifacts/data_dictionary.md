# Data Dictionary: Annual Temperature Anomalies Dataset

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Dataset:** Temperature Anomalies - Cleaned and Curated  
**Source:** Our World in Data (OWID) - Climate Change Data

---

## Overview

This data dictionary describes the cleaned and curated Annual Temperature Anomalies dataset, which contains global temperature deviation measurements from 1880 to 2023 for approximately 190 countries and regions.

---

## Table: TemperatureAnomalies

### Primary Key
- **Composite Key:** (`country_code`, `year`)
- **Uniqueness:** Each combination of country code and year appears exactly once in the cleaned dataset

---

## Column Descriptions

### 1. country
- **Type:** String (VARCHAR(100))
- **Description:** Full name of the country or geographical region
- **Format:** Free text, standardized during cleaning
- **Example Values:** "United States", "United Kingdom", "China", "World"
- **Missing Values:** Not allowed (required field)
- **Cleaning Notes:** 
  - Normalized using OpenRefine clustering (fingerprint + n-gram)
  - Standardized to match ISO country name conventions
- **Constraints:** 
  - Must not be null
  - Should match official country/region names

---

### 2. country_code
- **Type:** String (VARCHAR(3))
- **Description:** ISO 3166-1 alpha-3 (ISO-3) three-letter country code
- **Format:** Exactly 3 uppercase letters (A-Z)
- **Example Values:** "USA", "GBR", "CHN", "OWID_WRL" (for World aggregate)
- **Missing Values:** 
  - Original dataset: 15 records with missing codes
  - Cleaned dataset: Missing codes set to NULL for visibility in quality reports
- **Cleaning Notes:**
  - Standardized to uppercase
  - Mapped common aliases (e.g., "UK" → "GBR", "US" → "USA")
  - Validated against ISO-3 pattern (exactly 3 uppercase letters)
  - Invalid codes set to NULL
- **Constraints:**
  - Must match regex pattern: `^[A-Z]{3}$`
  - Part of composite primary key
- **Standards Reference:** ISO 3166-1 alpha-3

---

### 3. year
- **Type:** Integer (INT)
- **Description:** Calendar year for which the temperature anomaly is recorded
- **Format:** Four-digit year (YYYY)
- **Range:** 1880 - 2023
- **Example Values:** 1880, 1950, 2000, 2023
- **Missing Values:** Not allowed (required field)
- **Cleaning Notes:**
  - Coerced to integer type
  - Validated to be within expected temporal range
- **Constraints:**
  - Must be between 1880 and 2023 (inclusive)
  - Must not be null
  - Part of composite primary key

---

### 4. temperature_anomaly
- **Type:** Decimal (DECIMAL(7,6))
- **Description:** Annual temperature deviation from baseline reference period, measured in degrees Celsius (°C)
- **Format:** Decimal number with up to 6 decimal places
- **Units:** Degrees Celsius (°C)
- **Baseline Reference Period:** 1951-1980
- **Range:** Typically between -3.5°C and +5.0°C (extreme outliers flagged)
- **Example Values:** 
  - 0.5 (0.5°C above baseline)
  - -0.3 (-0.3°C below baseline)
  - 1.2 (1.2°C above baseline)
- **Missing Values:**
  - Original dataset: ~4,512 records (8.5% of dataset)
  - Missing data clustered in early decades (pre-1930) and under-reported regions
  - Missing values preserved as NULL in cleaned dataset (no imputation applied in initial cleaning)
- **Cleaning Notes:**
  - Coerced to numeric type
  - Outliers flagged (absolute value > 5°C) but not automatically removed
  - Negative values are valid (represent cooler years relative to baseline)
- **Constraints:**
  - Numeric type required
  - Values outside ±5°C range flagged as potential outliers
- **Interpretation:**
  - Positive values: warmer than baseline
  - Negative values: cooler than baseline
  - Zero: same as baseline average

---

## Data Quality Metrics

### Completeness
- **Total Records (after cleaning):** ~52,913 (after deduplication)
- **Missing temperature_anomaly:** ~4,512 records (8.5%)
- **Missing country_code:** 15 records (0.03%)

### Consistency
- **Duplicate Records Removed:** 87 duplicates (country, year pairs)
- **Country Code Standardization:** All codes validated against ISO-3 standard
- **Type Consistency:** All numeric fields properly typed

### Validity
- **Outlier Flags:** Records with |temperature_anomaly| > 5°C flagged for review
- **Year Range:** All years within 1880-2023
- **Country Code Format:** All codes match ISO-3 pattern (or NULL)

---

## Data Processing History

### Cleaning Steps Applied
1. **Column Standardization:** Mapped source column names to standard schema
2. **Country Code Normalization:** 
   - Uppercase conversion
   - Alias mapping (e.g., UK → GBR)
   - ISO-3 validation
3. **Type Coercion:** 
   - String fields: trimmed and standardized
   - Numeric fields: converted to appropriate types
4. **Deduplication:** Removed 87 duplicate (country_code, year) pairs
5. **Quality Reporting:** Generated DQ metrics without data mutation

### Tools Used
- **OpenRefine v3.9.5:** Initial cleaning and normalization
- **Python 3.8+ with Pandas 2.0+:** Automated cleaning pipeline

---

## Usage Notes

### Recommended Use Cases
- Long-term temperature trend analysis
- Regional climate change comparisons
- Global warming impact assessment
- Time series analysis (1880-2023)

### Limitations
- Missing data in early decades (pre-1930) may affect historical trend analysis
- Some regions have incomplete coverage
- Outliers require domain expertise to validate
- No imputation applied - missing values preserved as NULL

### Citation
When using this dataset, please cite:
- Original source: Our World in Data (CC BY 4.0)
- This curated version: Team 11, CS598 Data Cleaning, University of Illinois Urbana-Champaign (2025)

---

## Related Files
- `schema_definition.sql`: Database schema definition
- `temperature_anomalies_initial_clean.csv`: Cleaned dataset
- `temperature_anomalies_initial_dq_report.csv`: Data quality metrics
- `quality_profile_report.txt`: Detailed quality assessment

