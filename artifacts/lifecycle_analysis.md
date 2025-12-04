# Data Lifecycle Model Analysis

**Project:** End-to-End Data Curation Workflow for Climate Change Impact Data  
**Team 11 - CS598 Data Cleaning**  
**Date:** October 2025

---

## Executive Summary

This document maps our data curation workflow to established data lifecycle models, specifically the **DCC Curation Lifecycle Model** and the **OAIS Reference Model**. Our project demonstrates a complete data lifecycle from acquisition through preservation and dissemination.

---

## DCC Curation Lifecycle Model Mapping

The Digital Curation Centre (DCC) Curation Lifecycle Model provides a framework for understanding the stages of data curation. Our workflow aligns with the following phases:

### 1. **Create/Receive** (Data Acquisition)
**Our Implementation:**
- Downloaded raw dataset from Our World in Data (OWID)
- Verified data source authenticity and license (CC BY 4.0)
- Documented source URL and download date

**Artifacts:**
- Source data: OWID Climate Change dataset
- Documentation: README.md with source attribution

**Lifecycle Position:** Entry point into curation workflow

---

### 2. **Appraise/Select** (Quality Assessment)
**Our Implementation:**
- Conducted initial data profiling
- Identified quality issues:
  - Missing data (4,512 records, 8.5%)
  - Duplicate records (87 pairs)
  - Outliers (extreme temperature values)
  - Inconsistent country codes
- Documented findings in quality profile report

**Artifacts:**
- `quality_profile_report.txt`
- Quality metrics and issue documentation

**Lifecycle Position:** Decision point for data retention and cleaning strategy

---

### 3. **Ingest** (Schema Modeling)
**Our Implementation:**
- Defined relational schema for data integration
- Created `schema_definition.sql` with:
  - Table structure: `TemperatureAnomalies`
  - Primary key: (`country_code`, `year`)
  - Data types and constraints
- Established data model abstractions

**Artifacts:**
- `schema_definition.sql`
- Relational model documentation

**Lifecycle Position:** Structural organization of data

---

### 4. **Preserve** (Cleaning & Transformation)
**Our Implementation:**
- Applied two-stage cleaning pipeline:
  - **Stage 1:** OpenRefine normalization
  - **Stage 2:** Python/Pandas standardization
- Performed deduplication (removed 87 duplicates)
- Standardized country codes to ISO-3
- Enforced type consistency
- Generated cleaned dataset

**Artifacts:**
- `openrefine_operations.json`
- `initial_cleaning_script.py`
- `temperature_anomalies_initial_clean.csv`
- `temperature_anomalies_initial_dq_report.csv`

**Lifecycle Position:** Data preservation through quality improvement

---

### 5. **Store** (Output Generation)
**Our Implementation:**
- Generated cleaned CSV files
- Created data quality reports
- Maintained version control through Git
- Organized artifacts in structured directory

**Artifacts:**
- Cleaned datasets
- Quality reports
- Version-controlled repository

**Lifecycle Position:** Persistent storage of curated data

---

### 6. **Access/Reuse** (Documentation & Dissemination)
**Our Implementation:**
- Created comprehensive documentation:
  - Data dictionary
  - Metadata (DataCite format)
  - Provenance documentation
  - Workflow instructions
- Published on GitHub for public access
- Provided reproducibility instructions

**Artifacts:**
- `data_dictionary.md`
- `metadata_datacite.json`
- `provenance_workflow.md`
- `README.md`
- GitHub repository

**Lifecycle Position:** Enabling data reuse and reproducibility

---

### 7. **Transform** (Ongoing)
**Our Implementation:**
- Data transformation through cleaning scripts
- Schema standardization
- Format conversion (raw → cleaned CSV)

**Lifecycle Position:** Continuous throughout workflow

---

### 8. **Describe** (Ongoing)
**Our Implementation:**
- Metadata creation (DataCite)
- Data dictionary development
- Provenance documentation
- Quality reporting

**Lifecycle Position:** Continuous throughout workflow

---

## OAIS Reference Model Mapping

The Open Archival Information System (OAIS) model describes functional entities for digital preservation. Our workflow aligns with OAIS concepts:

### **Ingest Function**
- **Receive Submission Information Package (SIP):** Raw OWID data
- **Quality Assurance:** Data profiling and assessment
- **Generate Archival Information Package (AIP):** Cleaned dataset with metadata

### **Archival Storage**
- **Manage Storage Hierarchy:** Organized `/artifacts` directory
- **Replace Media:** Version control through Git
- **Error Checking:** Data quality validation

### **Data Management**
- **Administer Database:** Schema definition and management
- **Perform Queries:** Data dictionary and metadata
- **Generate Reports:** Quality reports and provenance

### **Access Function**
- **Receive Requests:** GitHub repository access
- **Generate Dissemination Information Package (DIP):** Cleaned datasets and documentation
- **Deliver Response:** Public repository with complete artifacts

### **Preservation Planning**
- **Monitor Designated Community:** Climate research community needs
- **Develop Preservation Strategies:** Standard formats (CSV, SQL)
- **Monitor Technology:** Python/Pandas ecosystem

### **Administration**
- **Negotiate Submission Agreement:** CC BY 4.0 license compliance
- **Audit Submission:** Quality assessment
- **Establish Standards:** ISO-3, DataCite standards

---

## Lifecycle Model Comparison

| DCC Phase | OAIS Function | Our Implementation |
|-----------|---------------|-------------------|
| Create/Receive | Ingest (SIP) | OWID data download |
| Appraise/Select | Ingest (QA) | Quality assessment |
| Ingest | Data Management | Schema definition |
| Preserve | Archival Storage | Cleaning & storage |
| Store | Archival Storage | Output generation |
| Access/Reuse | Access (DIP) | Documentation & GitHub |
| Transform | Ingest/Archival | Data cleaning |
| Describe | Data Management | Metadata creation |

---

## Workflow Phases vs. Lifecycle Models

### Phase 1: Data Acquisition & Modeling
- **DCC:** Create/Receive + Ingest
- **OAIS:** Ingest (SIP) + Data Management
- **Activities:** Download, verify, schema definition

### Phase 2: Quality Assessment
- **DCC:** Appraise/Select
- **OAIS:** Ingest (QA)
- **Activities:** Profiling, issue identification

### Phase 3: Cleaning & Transformation
- **DCC:** Preserve + Transform
- **OAIS:** Ingest (AIP generation)
- **Activities:** OpenRefine + Python cleaning

### Phase 4: Documentation & Reproducibility
- **DCC:** Access/Reuse + Describe
- **OAIS:** Access (DIP) + Data Management
- **Activities:** Metadata, documentation, GitHub

---

## Lifecycle Continuity

Our workflow demonstrates **iterative refinement** across lifecycle phases:

1. **Initial Assessment** → Identified issues
2. **Cleaning** → Addressed issues
3. **Quality Reporting** → Validated improvements
4. **Documentation** → Enabled reuse

This iterative approach ensures data quality improves at each lifecycle stage.

---

## References

- Digital Curation Centre. (n.d.). *DCC Curation Lifecycle Model*. https://www.dcc.ac.uk/guidance/curation-lifecycle-model
- Consultative Committee for Space Data Systems. (2012). *Reference Model for an Open Archival Information System (OAIS)*. ISO 14721:2012.
- Ball, A. (2010). *Review of Data Management Lifecycle Models*. University of Bath.

---

## Conclusion

Our data curation workflow successfully implements key phases of both the DCC Curation Lifecycle Model and OAIS Reference Model. The workflow demonstrates:

- **Complete lifecycle coverage:** From acquisition to dissemination
- **Iterative quality improvement:** Assessment → Cleaning → Validation
- **Preservation focus:** Standard formats, metadata, documentation
- **Reusability:** Public repository with complete artifacts

This alignment with established lifecycle models ensures our curated dataset follows best practices for long-term preservation and reuse.

