# Data Concepts and Practices Analysis

**Project:** End-to-End Data Curation Workflow for Climate Change Impact Data  
**Team 11 - CS598 Data Cleaning**  
**Date:** October 2025

---

## Executive Summary

This document relates our data curation project to fundamental data concepts, specifically the **Basic Representation Model (BRM)** and **data practices** research. We analyze how our dataset represents information, the abstractions we employ, and the curation practices that align with data stewardship principles.

---

## Part 1: Data Concepts (M7) - Basic Representation Model (BRM)

### Understanding the BRM

The Basic Representation Model (BRM) provides a framework for understanding how data represents information. It distinguishes between:

1. **Information Object:** The conceptual information being represented
2. **Data Object:** The physical or digital representation
3. **Representation Information:** Metadata needed to interpret the data object

### BRM Application to Our Dataset

#### Information Object
**Conceptual Level:** The information we represent is:
- **Entity:** Annual temperature anomalies for countries/regions
- **Attributes:** Country, country code, year, temperature deviation
- **Relationships:** Country-Year pairs with associated temperature measurements
- **Domain:** Climate science, global temperature trends

**Example:** "The United States in 2020 had a temperature anomaly of +1.2°C relative to the 1951-1980 baseline."

#### Data Object
**Physical Representation:** 
- **Format:** CSV files (comma-separated values)
- **Structure:** Tabular format with rows and columns
- **Encoding:** UTF-8 text encoding
- **Storage:** Digital files in GitHub repository

**Example Row:**
```
country,country_code,year,temperature_anomaly
United States,USA,2020,1.2
```

#### Representation Information
**Metadata Required for Interpretation:**

1. **Schema Information:**
   - Column names and meanings
   - Data types (string, integer, decimal)
   - Constraints (primary key, valid ranges)

2. **Semantic Information:**
   - Temperature anomaly definition (deviation from baseline)
   - Baseline period (1951-1980)
   - Units (degrees Celsius)
   - Country code standard (ISO-3)

3. **Provenance Information:**
   - Source (Our World in Data)
   - Processing history (cleaning steps)
   - Version information

4. **Context Information:**
   - Temporal coverage (1880-2023)
   - Spatial coverage (global, ~190 countries)
   - Data quality issues (missing values, outliers)

**Our Documentation Provides:**
- `schema_definition.sql` - Structural representation
- `data_dictionary.md` - Semantic representation
- `metadata_datacite.json` - Standardized metadata
- `provenance_workflow.md` - Processing history

### BRM Layers in Our Project

#### Layer 1: Physical Representation
- **CSV files:** Raw bytes stored as text
- **File system:** Directory structure in repository
- **Version control:** Git repository

#### Layer 2: Logical Representation
- **Relational schema:** Table structure (TemperatureAnomalies)
- **Data types:** VARCHAR, INT, DECIMAL
- **Constraints:** Primary key, data ranges

#### Layer 3: Conceptual Representation
- **Entities:** Countries, Years, Temperature Anomalies
- **Relationships:** Country-Year associations
- **Domain concepts:** Climate change, temperature trends

#### Layer 4: Semantic Representation
- **Meaning:** Temperature deviation from baseline
- **Interpretation:** Positive = warmer, Negative = cooler
- **Context:** Climate change impact analysis

### Value-Level vs. Structure-Level Considerations

#### Value-Level (Data Content)
- **Individual values:** "USA", 2020, 1.2
- **Data quality:** Missing values, outliers, duplicates
- **Cleaning focus:** Correcting individual data points

**Our Approach:**
- Identified and documented missing values (4,512 records)
- Flagged outliers (|anomaly| > 5°C)
- Removed duplicate values (87 pairs)

#### Structure-Level (Data Organization)
- **Schema design:** Table structure, column definitions
- **Relationships:** Primary keys, foreign keys
- **Constraints:** Data types, valid ranges

**Our Approach:**
- Defined relational schema with composite primary key
- Established data type constraints
- Standardized column names and formats

### BRM and Data Quality

The BRM helps us understand data quality issues:

1. **Missing Representation Information:**
   - Problem: Missing country codes (15 records)
   - Impact: Cannot interpret which country the data represents
   - Solution: Set to NULL, document in quality report

2. **Incomplete Data Objects:**
   - Problem: Missing temperature values (4,512 records)
   - Impact: Cannot represent complete information
   - Solution: Preserve NULLs, document coverage gaps

3. **Inconsistent Representation:**
   - Problem: Country code variations (UK vs GBR)
   - Impact: Same entity represented differently
   - Solution: Standardize to ISO-3 format

---

## Part 2: Data Practices (M13)

### Data Practices Research Framework

Data practices research examines how data is created, managed, and used in research contexts. Our project demonstrates several key data practices:

### 1. **Data Curation Practices**

#### Documentation Practice
**What we do:**
- Create comprehensive metadata (DataCite)
- Develop detailed data dictionary
- Document provenance and workflow
- Maintain version control

**Why it matters:**
- Enables data reuse
- Ensures reproducibility
- Supports long-term preservation

#### Quality Assurance Practice
**What we do:**
- Systematic quality assessment
- Issue identification and documentation
- Cleaning and validation
- Quality reporting

**Why it matters:**
- Ensures data reliability
- Identifies limitations
- Supports informed use

#### Standardization Practice
**What we do:**
- Use ISO-3 country codes
- Follow DataCite metadata schema
- Apply SQL schema standards
- Maintain consistent formats

**Why it matters:**
- Enables integration
- Facilitates interoperability
- Supports automated processing

### 2. **Data Stewardship Practices**

#### Transparency Practice
**What we do:**
- Document all processing steps
- Preserve original and cleaned versions
- Provide complete provenance chain
- Open repository (GitHub)

**Why it matters:**
- Builds trust
- Enables verification
- Supports reproducibility

#### Preservation Practice
**What we do:**
- Use standard formats (CSV, SQL)
- Create persistent metadata
- Version control
- Public archiving (GitHub)

**Why it matters:**
- Ensures long-term access
- Prevents data loss
- Supports future use

#### Ethical Practice
**What we do:**
- Maintain source attribution (CC BY 4.0)
- Document data limitations
- Provide usage guidelines
- Respect intellectual property

**Why it matters:**
- Legal compliance
- Ethical research conduct
- Community trust

### 3. **Research Data Management Practices**

#### Organization Practice
**What we do:**
- Structured directory (`/artifacts`)
- Consistent naming conventions
- Logical file organization
- Clear documentation structure

**Why it matters:**
- Facilitates navigation
- Reduces errors
- Improves efficiency

#### Reproducibility Practice
**What we do:**
- Automated scripts (Python)
- Documented operations (OpenRefine JSON)
- Environment specification (requirements.txt)
- Step-by-step instructions

**Why it matters:**
- Enables verification
- Supports replication
- Builds confidence

#### Collaboration Practice
**What we do:**
- Team-based workflow
- Shared repository
- Version control
- Clear documentation

**Why it matters:**
- Enables teamwork
- Tracks contributions
- Maintains consistency

### 4. **Data Lifecycle Practices**

#### Acquisition Practice
- Source verification
- License compliance
- Initial assessment

#### Processing Practice
- Systematic cleaning
- Quality validation
- Transformation documentation

#### Preservation Practice
- Standard formats
- Metadata creation
- Long-term storage

#### Dissemination Practice
- Public repository
- Complete documentation
- Usage guidelines

### 5. **Domain-Specific Practices (Climate Science)**

#### Scientific Data Practices
**What we do:**
- Preserve original measurements
- Document baseline references
- Flag outliers for expert review
- Maintain temporal integrity

**Why it matters:**
- Scientific accuracy
- Research validity
- Reproducible analysis

#### Climate Data Practices
**What we do:**
- Use standard temperature units (°C)
- Document baseline period (1951-1980)
- Preserve spatial coverage (global)
- Maintain temporal coverage (1880-2023)

**Why it matters:**
- Enables comparison
- Supports trend analysis
- Facilitates integration

### Data Practices Alignment with Principles

Our practices align with key data stewardship principles:

1. **FAIR Principles:**
   - **Findable:** GitHub repository, metadata
   - **Accessible:** Public access, standard formats
   - **Interoperable:** Standard schemas, ISO codes
   - **Reusable:** Complete documentation, clear license

2. **CARE Principles (for Indigenous Data):**
   - While not directly applicable, we respect data sovereignty through proper attribution

3. **Open Science Principles:**
   - Open access repository
   - Transparent methodology
   - Reproducible workflow
   - Public documentation

### Challenges and Adaptations

#### Challenge: Missing Data
**Practice Adaptation:**
- Document rather than impute
- Preserve NULLs for transparency
- Flag in quality reports

#### Challenge: Data Heterogeneity
**Practice Adaptation:**
- Standardize to common formats
- Map variations to standards
- Document transformations

#### Challenge: Reproducibility
**Practice Adaptation:**
- Automated scripts
- Version control
- Complete documentation

---

## Integration: BRM and Data Practices

### How BRM Informs Our Practices

1. **Representation Information → Documentation Practice:**
   - BRM emphasizes need for metadata
   - We create comprehensive documentation

2. **Data Object Structure → Standardization Practice:**
   - BRM highlights structure importance
   - We standardize schemas and formats

3. **Information Object → Quality Practice:**
   - BRM focuses on accurate representation
   - We assess and improve data quality

### How Practices Support BRM

1. **Documentation → Representation Information:**
   - Practices ensure complete metadata
   - Supports BRM interpretation needs

2. **Standardization → Consistent Representation:**
   - Practices ensure uniform structure
   - Supports BRM data object consistency

3. **Quality Assurance → Accurate Representation:**
   - Practices improve data accuracy
   - Supports BRM information object fidelity

---

## References

- Borgman, C. L. (2015). *Big Data, Little Data, No Data: Scholarship in the Networked World*. MIT Press.
- Borgman, C. L., Scharnhorst, A., & Golshan, M. S. (2019). Digital data archives as knowledge infrastructures: Mediating data sharing and reuse. *Journal of the Association for Information Science and Technology*, 70(8), 888-904.
- Consultative Committee for Space Data Systems. (2012). *Reference Model for an Open Archival Information System (OAIS)*. ISO 14721:2012.
- Leonelli, S. (2016). *Data-Centric Biology: A Philosophical Study*. University of Chicago Press.
- Pasquetto, I. V., Randles, B. M., & Borgman, C. L. (2017). On the reuse of scientific data. *Data Science Journal*, 16, 8.
- Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.

---

## Conclusion

Our data curation project demonstrates alignment with fundamental data concepts (BRM) and established data practices. By understanding data representation at multiple levels and applying systematic curation practices, we create a dataset that is:

- **Well-represented:** Complete representation information
- **Well-documented:** Comprehensive metadata and documentation
- **Well-preserved:** Standard formats and persistent storage
- **Well-usable:** Clear structure and usage guidelines

This integration of concepts and practices ensures our curated dataset serves as a reliable foundation for climate change research and analysis.

