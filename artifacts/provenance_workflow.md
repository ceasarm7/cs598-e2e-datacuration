# Data Provenance and Workflow Documentation

**Project:** End-to-End Data Curation Workflow for Climate Change Impact Data  
**Team 11 - CS598 Data Cleaning**  
**Date:** October 2025  
**Version:** 1.0.0

---

## Executive Summary

This document describes the complete data provenance chain and reproducible workflow for curating the Annual Temperature Anomalies dataset. The workflow transforms raw data from Our World in Data into a cleaned, standardized, and documented dataset suitable for climate change research.

---

## Data Lineage

### Source Data
- **Origin:** Our World in Data (OWID) - Climate Change Data
- **URL:** https://ourworldindata.org/climate-change
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Format:** CSV
- **Download Date:** [To be filled]
- **Original Schema:**
  - Entity (country name)
  - Code (country code)
  - Year
  - Temperature anomaly

### Processing Chain

```
Raw OWID Data (CSV)
    ↓
[Phase 1: Data Acquisition & Modeling]
    ↓
Schema Definition (schema_definition.sql)
    ↓
[Phase 2: Quality Assessment]
    ↓
Quality Profile Report (quality_profile_report.txt)
    ↓
[Phase 3: Cleaning & Transformation]
    ├─→ OpenRefine Pipeline (openrefine_operations.json)
    │   └─→ temperature_anomalies_refine_clean_base.csv
    │
    └─→ Python/Pandas Pipeline (initial_cleaning_script.py)
        ├─→ temperature_anomalies_initial_clean.csv
        └─→ temperature_anomalies_initial_dq_report.csv
    ↓
[Phase 4: Documentation & Reproducibility]
    ├─→ Data Dictionary (data_dictionary.md)
    ├─→ Metadata (metadata_datacite.json)
    └─→ This Provenance Document
```

---

## Detailed Workflow Steps

### Phase 1: Data Acquisition & Modeling

**Objective:** Acquire raw data and define target schema

**Actions:**
1. Downloaded dataset from Our World in Data website
2. Verified data integrity and completeness
3. Defined relational schema (`schema_definition.sql`)
   - Table: `TemperatureAnomalies`
   - Primary Key: (`country_code`, `year`)
   - Columns: country, country_code, year, temperature_anomaly

**Artifacts:**
- `schema_definition.sql`

**Tools:** Manual download, SQL schema design

---

### Phase 2: Quality Assessment

**Objective:** Identify data quality issues and document findings

**Actions:**
1. Initial data profiling
2. Identified quality issues:
   - Missing data: 4,512 records (8.5%) in temperature_anomaly
   - Missing country codes: 15 records
   - Duplicate records: 87 (country, year) pairs
   - Outliers: Extreme values (> ±5°C)
3. Documented findings in quality profile report

**Artifacts:**
- `quality_profile_report.txt`

**Tools:** Manual inspection, statistical analysis

---

### Phase 3: Cleaning & Transformation

#### 3.1 OpenRefine Pipeline

**Objective:** Initial cleaning and normalization

**Tool:** OpenRefine v3.9.5

**Operations (see `openrefine_operations.json`):**
1. **Country Code Transformation:**
   - Expression: `grel:value.trim().toUppercase().replace(/[^A-Z]/, "")`
   - Purpose: Standardize country codes to uppercase, remove non-alphabetic characters

2. **Year Type Coercion:**
   - Expression: `value.toNumber()`
   - Purpose: Convert year to numeric type

3. **Temperature Anomaly Type Coercion:**
   - Expression: `value.toNumber()`
   - Purpose: Convert temperature anomaly to numeric type

4. **Composite Key Creation:**
   - Expression: `grel:cells["Code"].value + "-" + cells["Year"].value.toString()`
   - New Column: `key_code_year`
   - Purpose: Create unique identifier for deduplication

5. **Duplicate Removal:**
   - Criteria: Based on `Entity` (country name)
   - Purpose: Remove obvious duplicates

6. **Outlier Flagging:**
   - Expression: `grel:if(isBlank(value), "no", if(abs(value) > 5, "yes", "no"))`
   - New Column: `outlier_flag`
   - Purpose: Flag potential outliers for review

**Input:** Raw OWID CSV data  
**Output:** `temperature_anomalies_refine_clean_base.csv`

**Artifacts:**
- `openrefine_operations.json` (exported operations)
- `temperature_anomalies_refine_clean_base.csv`

---

#### 3.2 Python/Pandas Pipeline

**Objective:** Automated cleaning, standardization, and quality reporting

**Tool:** Python 3.8+ with Pandas 2.0+

**Script:** `initial_cleaning_script.py`

**Processing Steps:**

1. **Load and Standardize Columns** (`load_and_standardize_columns`)
   - Maps source column names to standard schema
   - Handles both OpenRefine output and raw OWID formats
   - Validates required columns present

2. **Country Code Standardization** (`standardize_country_codes`)
   - Converts to uppercase string
   - Maps common aliases to ISO-3 codes (e.g., "UK" → "GBR", "US" → "USA")
   - Validates ISO-3 format (exactly 3 uppercase letters)
   - Sets invalid codes to NULL

3. **Type Coercion** (`coerce_types`)
   - Country: String, trimmed
   - Year: Integer (nullable Int64)
   - Temperature anomaly: Numeric (float)

4. **Deduplication** (`enforce_uniqueness`)
   - Removes duplicates based on (country_code, year)
   - Keeps first occurrence
   - Reports number of duplicates removed

5. **Quality Reporting** (`make_initial_dq_report`)
   - Generates data quality metrics
   - No data mutation (read-only analysis)
   - Reports: row counts, unique countries, year ranges, missing values

**Input:** `temperature_anomalies_refine_clean_base.csv`  
**Outputs:**
- `temperature_anomalies_initial_clean.csv` (cleaned dataset)
- `temperature_anomalies_initial_dq_report.csv` (quality metrics)

**Artifacts:**
- `initial_cleaning_script.py`

---

### Phase 4: Documentation & Reproducibility

**Objective:** Create comprehensive documentation for reuse and reproducibility

**Actions:**
1. Created data dictionary with detailed column descriptions
2. Generated DataCite metadata JSON
3. Documented provenance and workflow
4. Created environment specification (requirements.txt)
5. Updated README with installation and usage instructions

**Artifacts:**
- `data_dictionary.md`
- `metadata_datacite.json`
- `provenance_workflow.md` (this document)
- `requirements.txt`
- `README.md`

---

## Reproducibility Instructions

### Prerequisites
- Python 3.8 or higher
- OpenRefine v3.9.5 (for OpenRefine pipeline)
- Internet connection (for downloading source data)

### Installation

1. **Clone Repository:**
   ```bash
   git clone https://github.com/ceasarm7/cs598-e2e-datacuration.git
   cd cs598-e2e-datacuration
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Source Data:**
   - Visit https://ourworldindata.org/climate-change
   - Download Annual Temperature Anomalies dataset
   - Place in `artifacts/` directory

### Running the Workflow

#### Option 1: OpenRefine Pipeline (Manual)
1. Open OpenRefine v3.9.5
2. Import raw OWID CSV file
3. Import operations from `artifacts/openrefine_operations.json`
4. Apply operations
5. Export as `temperature_anomalies_refine_clean_base.csv`

#### Option 2: Python Pipeline (Automated)
1. Ensure `temperature_anomalies_refine_clean_base.csv` exists in `artifacts/` directory
2. Run cleaning script:
   ```bash
   cd artifacts
   python initial_cleaning_script.py
   ```
3. Outputs will be generated in the same directory:
   - `temperature_anomalies_initial_clean.csv`
   - `temperature_anomalies_initial_dq_report.csv`

### Expected Results
- Cleaned dataset with standardized schema
- Duplicate records removed (87 duplicates)
- Country codes normalized to ISO-3
- Data quality report with metrics

---

## Version Control

### Dataset Versions
- **v1.0.0 (Current):** Initial cleaned version
  - OpenRefine + Python cleaning applied
  - 87 duplicates removed
  - ISO-3 country code standardization
  - No imputation applied (missing values preserved)

### Future Versions (Planned)
- **v1.1.0:** Statistical outlier handling (z-scores)
- **v1.2.0:** Missing value imputation (interpolation)
- **v2.0.0:** Final production-ready version with comprehensive DQ report

---

## Ethical and Legal Considerations

### License Compliance
- **Source License:** CC BY 4.0 (Our World in Data)
- **Derived Work License:** CC BY 4.0 (maintains attribution requirement)
- **Attribution:** All outputs include source attribution to OWID

### Data Privacy
- No personal or sensitive data in dataset
- Publicly available climate data
- No privacy concerns

### Ethical Use
- Dataset suitable for climate change research
- No ethical restrictions on use
- Encouraged for educational and research purposes

---

## Quality Assurance

### Validation Checks
1. **Schema Validation:** All columns match defined schema
2. **Type Validation:** All fields have correct data types
3. **Constraint Validation:** Primary key uniqueness enforced
4. **Range Validation:** Years within 1880-2023, country codes ISO-3 format
5. **Completeness Check:** Missing value counts documented

### Known Issues
- Missing data in early decades (pre-1930): ~8.5% of records
- Some outliers require domain expert validation
- 15 records with missing country codes (set to NULL)

---

## References and Standards

### Standards Used
- **ISO 3166-1 alpha-3:** Country code standard
- **DataCite Schema v4:** Metadata standard
- **SQL:** Schema definition language
- **CSV:** Data exchange format

### Tools and Libraries
- **OpenRefine v3.9.5:** Data cleaning tool
- **Python 3.8+:** Programming language
- **Pandas 2.0+:** Data manipulation library

### Related Documentation
- Our World in Data: https://ourworldindata.org/climate-change
- ISO 3166-1: https://www.iso.org/iso-3166-country-codes.html
- DataCite Schema: https://schema.datacite.org/

---

## Contact and Support

**Team 11 - CS598 Data Cleaning**
- Cesar Mancillas: cam37@illinois.edu
- Aristofanes Cruz: ac163@illinois.edu
- Cesar Nava: can14@illinois.edu

**Repository:** https://github.com/ceasarm7/cs598-e2e-datacuration

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | October 2025 | Initial provenance documentation |

