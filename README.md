# cs598-e2e-datacuration
team work for the "End-to-End Data Curation Workflow" for climate change 
# End-to-End Data Curation Workflow for Climate Change Impact Data

## Team 11 — CS598 Data Cleaning

**Team Members**
- Cesar Mancillas — UIN: 651066529 — 📧 cam37@illinois.edu  
- Aristofanes Cruz — UIN: 655558479 — 📧 ac163@illinois.edu  
- Cesar Nava — UIN: 654326785 — 📧 can14@illinois.edu  

📂 **Repository:** [https://github.com/ceasarm7/cs598-e2e-datacuration](https://github.com/ceasarm7/cs598-e2e-datacuration)

---

## 📘 Project Overview

This project develops an **end-to-end data curation workflow** for *Climate Change Impact Data*, focusing on the **Annual Temperature Anomalies** dataset from *Our World in Data (OWID)*.

The workflow demonstrates how to:
1. Acquire and model raw open data.
2. Assess data quality.
3. Clean, transform, and document reproducible datasets.
4. Generate evidence-based, quality-assured outputs ready for analysis.

All work is guided by the main use case (**U1**):  
> “Analyze long-term regional and global temperature trends to understand the impact of climate change.”

---

## 🧩 Dataset Description

**Source:** [Our World in Data – Climate Change Data](https://ourworldindata.org/climate-change)  
**License:** CC BY 4.0  
**Primary Table:** `TemperatureAnomalies`

| Column | Description |
|---------|--------------|
| `country` | Country or region name |
| `country_code` | ISO-3 code for the country |
| `year` | Year of record |
| `temperature_anomaly` | Annual deviation (°C) from baseline (e.g., 1951–1980) |

### Data Extent
- **Spatial:** Global coverage (~190 countries)
- **Temporal:** 1880–2023

---

## ⚙️ Workflow Summary

The data curation workflow includes four main phases:

### 1. Data Acquisition & Modeling
- Dataset downloaded and verified from OWID.
- Relational schema defined (`schema_definition.sql`) for integration.

### 2. Quality Assessment
- Initial profiling identified:
  - Missing data (especially early 20th century)
  - Inconsistent baselines
  - Duplicate (country, year) records
  - Outlier temperature anomalies (> ±5°C)

### 3. Cleaning & Transformation
Two complementary pipelines:
- **OpenRefine (v3.9.5)**
  - Country name normalization
  - Type coercion (year, anomaly)
  - Composite key creation
  - Clustering (fingerprint + n-gram)
  - Export: `temperature_anomalies_refine_clean_base.csv`

- **Python/Pandas**
  - Automated schema enforcement
  - Country code ISO-3 normalization
  - Deduplication
  - Lightweight Data Quality (DQ) report
  - Outputs:
    - `temperature_anomalies_initial_clean.csv`
    - `temperature_anomalies_initial_dq_report.csv`

### 4. Documentation & Reproducibility
All operations, scripts, and outputs are stored under `/artifacts`.

---

## 🧾 Repository Structure

