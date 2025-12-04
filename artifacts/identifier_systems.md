# Identity and Identifier Systems Analysis

**Project:** End-to-End Data Curation Workflow for Climate Change Impact Data  
**Team 11 - CS598 Data Cleaning**  
**Date:** October 2025

---

## Executive Summary

This document describes the identifier systems used in our data curation project, focusing on country identification through ISO-3 codes, composite primary keys, and the rationale for identifier selection. We analyze identifier requirements, alternatives considered, and implementation decisions.

---

## Identifier Requirements

### Functional Requirements

1. **Uniqueness:** Each country-year combination must be uniquely identifiable
2. **Stability:** Identifiers should remain consistent over time
3. **Standardization:** Use recognized international standards
4. **Interoperability:** Enable integration with other datasets
5. **Human Readability:** Support both machine and human interpretation

### Domain Requirements

1. **Country Identification:** Uniquely identify ~190 countries/regions
2. **Temporal Identification:** Uniquely identify years (1880-2023)
3. **Composite Identification:** Uniquely identify country-year pairs
4. **Integration:** Support joining with other climate datasets

---

## Primary Identifier: ISO 3166-1 Alpha-3 (ISO-3)

### Selection

**Chosen Identifier:** ISO 3166-1 alpha-3 country codes (ISO-3)

**Format:** Three uppercase letters (A-Z)

**Examples:**
- `USA` - United States
- `GBR` - United Kingdom
- `CHN` - China
- `OWID_WRL` - World aggregate (OWID-specific)

### Justification

#### 1. **International Standard**
- **Authority:** International Organization for Standardization (ISO)
- **Recognition:** Widely adopted in international data systems
- **Maintenance:** Regularly updated by ISO
- **Reliability:** Official standard with governance

**Why this matters:**
- Ensures interoperability with other datasets
- Provides authoritative country identification
- Supports long-term data preservation

#### 2. **Stability**
- **Persistence:** Codes remain stable even when country names change
- **Historical continuity:** Supports historical data analysis
- **Future-proof:** Less likely to change than country names

**Example:**
- Country name: "Myanmar" (formerly "Burma")
- ISO-3 code: `MMR` (stable across name changes)

#### 3. **Uniqueness**
- **Coverage:** Unique code for each country/territory
- **Completeness:** Covers all countries in our dataset
- **No ambiguity:** Single code per country

**Why this matters:**
- Prevents identification conflicts
- Enables reliable joins and merges
- Supports automated processing

#### 4. **Compactness**
- **Length:** Exactly 3 characters
- **Efficiency:** Minimal storage overhead
- **Readability:** Short enough for human recognition

**Comparison:**
- ISO-3: `USA` (3 chars)
- Country name: "United States" (13 chars)
- ISO-2: `US` (2 chars, but less specific)

#### 5. **Interoperability**
- **Integration:** Compatible with other climate datasets
- **Standards alignment:** Used by major data providers
- **Tool support:** Supported by data processing tools

**Examples:**
- World Bank data uses ISO-3
- UN datasets use ISO-3
- Climate research datasets use ISO-3

### Implementation

#### Standardization Process

1. **Uppercase Conversion:**
   ```python
   df["country_code"] = df["country_code"].str.upper()
   ```

2. **Alias Mapping:**
   ```python
   code_map = {
       "UK": "GBR",
       "US": "USA",
       "KOREA, REP.": "KOR",
       # ... additional mappings
   }
   ```

3. **Format Validation:**
   ```python
   iso3_mask = df["country_code"].str.fullmatch(r"[A-Z]{3}", na=False)
   ```

4. **Invalid Code Handling:**
   - Set non-ISO-3 codes to NULL
   - Document in quality reports
   - Flag for manual review

#### Challenges Addressed

1. **Missing Codes (15 records):**
   - Set to NULL
   - Documented in quality report
   - Preserved for manual resolution

2. **Code Variations:**
   - Mapped aliases to ISO-3
   - Standardized format
   - Validated against pattern

3. **Special Cases:**
   - OWID aggregates (e.g., "World") use `OWID_WRL`
   - Preserved for completeness
   - Documented in data dictionary

---

## Composite Primary Key: (country_code, year)

### Selection

**Chosen Identifier:** Composite primary key combining `country_code` and `year`

**Format:** 
- `country_code`: ISO-3 (3 uppercase letters)
- `year`: Integer (1880-2023)
- **Combined:** `(country_code, year)` tuple

**Examples:**
- `(USA, 2020)` - United States in 2020
- `(GBR, 1950)` - United Kingdom in 1950
- `(CHN, 2000)` - China in 2000

### Justification

#### 1. **Uniqueness Requirement**
- **Problem:** Single country code insufficient (multiple years per country)
- **Solution:** Combine country and year for unique identification
- **Result:** Each country-year pair uniquely identified

**Why this matters:**
- Prevents duplicate records
- Enables reliable data operations
- Supports temporal analysis

#### 2. **Natural Key**
- **Semantic meaning:** Reflects actual data structure
- **Domain alignment:** Matches research use case
- **Intuitive:** Easy to understand and use

**Alternative (Surrogate Key):**
- Could use auto-incrementing ID
- Less meaningful
- Requires additional joins

#### 3. **Query Efficiency**
- **Indexing:** Supports efficient queries by country or year
- **Filtering:** Enables fast country-year lookups
- **Joins:** Facilitates temporal joins

**Example Query:**
```sql
SELECT * FROM TemperatureAnomalies 
WHERE country_code = 'USA' AND year = 2020;
```

#### 4. **Data Integrity**
- **Constraint enforcement:** Prevents duplicate country-year pairs
- **Referential integrity:** Supports foreign key relationships
- **Validation:** Enables automated duplicate detection

**Implementation:**
```sql
PRIMARY KEY (country_code, year)
```

### Implementation

#### Schema Definition
```sql
CREATE TABLE TemperatureAnomalies (
    country VARCHAR(100),
    country_code VARCHAR(3),
    year INT,
    temperature_anomaly DECIMAL(7,6),
    PRIMARY KEY (country_code, year)
);
```

#### Deduplication Process
```python
df = df.drop_duplicates(
    subset=["country_code", "year"], 
    keep="first"
)
```

**Result:** Removed 87 duplicate country-year pairs

---

## Alternative Identifiers Considered

### 1. ISO 3166-1 Alpha-2 (ISO-2)

**Format:** Two uppercase letters (e.g., `US`, `GB`, `CN`)

**Advantages:**
- Shorter (2 vs 3 characters)
- More commonly used in some contexts
- Slightly more compact

**Disadvantages:**
- Less specific (fewer unique codes)
- Some countries share similar codes
- Less standard in climate data
- Reduced interoperability

**Decision:** Rejected - ISO-3 provides better specificity and interoperability

---

### 2. Country Names

**Format:** Full country names (e.g., "United States", "United Kingdom")

**Advantages:**
- Human readable
- No standardization needed
- Intuitive

**Disadvantages:**
- Not stable (name changes)
- Language dependent
- Ambiguous (multiple names)
- Not machine-friendly
- Inefficient for joins

**Decision:** Rejected - Unstable and inefficient

---

### 3. Numeric Country Codes

**Format:** Numeric codes (e.g., 840 for USA, 826 for GBR)

**Advantages:**
- Compact (3 digits)
- Machine efficient
- Some standards use numeric

**Disadvantages:**
- Not human readable
- Less common in climate data
- Requires lookup tables
- Less intuitive

**Decision:** Rejected - Less interoperable with climate datasets

---

### 4. Surrogate Keys (Auto-incrementing IDs)

**Format:** Sequential integers (1, 2, 3, ...)

**Advantages:**
- Simple
- Guaranteed uniqueness
- Efficient storage

**Disadvantages:**
- No semantic meaning
- Requires additional joins
- Less intuitive
- Doesn't reflect data structure

**Decision:** Rejected - Natural composite key more appropriate

---

### 5. UUIDs (Universally Unique Identifiers)

**Format:** 128-bit identifiers (e.g., `550e8400-e29b-41d4-a716-446655440000`)

**Advantages:**
- Globally unique
- No coordination needed
- Standard format

**Disadvantages:**
- Very long (36 characters)
- Not human readable
- No semantic meaning
- Overkill for this use case

**Decision:** Rejected - Unnecessary complexity for structured data

---

## Identifier System Architecture

### Hierarchical Structure

```
Dataset: TemperatureAnomalies
    │
    ├─ Country Level
    │   └─ Identifier: country_code (ISO-3)
    │       └─ Examples: USA, GBR, CHN
    │
    ├─ Temporal Level
    │   └─ Identifier: year (Integer)
    │       └─ Range: 1880-2023
    │
    └─ Composite Level
        └─ Identifier: (country_code, year)
            └─ Examples: (USA, 2020), (GBR, 1950)
```

### Identifier Relationships

1. **Country Code → Country Name:**
   - One-to-one mapping
   - ISO-3 uniquely identifies country
   - Country name provides human-readable label

2. **Country Code + Year → Temperature Anomaly:**
   - Composite key uniquely identifies measurement
   - Enables temporal analysis
   - Supports country-specific trends

3. **Year → Multiple Countries:**
   - One year has many country records
   - Enables cross-country comparison
   - Supports global trend analysis

---

## Identifier Validation and Quality

### Validation Rules

1. **ISO-3 Format:**
   - Pattern: `^[A-Z]{3}$`
   - Exactly 3 uppercase letters
   - No numbers or special characters

2. **Year Range:**
   - Minimum: 1880
   - Maximum: 2023
   - Integer type

3. **Composite Uniqueness:**
   - No duplicate (country_code, year) pairs
   - Enforced by primary key constraint

### Quality Issues Addressed

1. **Missing Country Codes (15 records):**
   - **Issue:** NULL country_code values
   - **Action:** Set to NULL, documented
   - **Impact:** Cannot uniquely identify country

2. **Invalid Format:**
   - **Issue:** Non-ISO-3 codes (e.g., "UK", "US")
   - **Action:** Mapped to ISO-3 or set to NULL
   - **Impact:** Standardization achieved

3. **Duplicates:**
   - **Issue:** 87 duplicate (country, year) pairs
   - **Action:** Removed duplicates, kept first occurrence
   - **Impact:** Uniqueness enforced

---

## Identifier Usage in Workflow

### 1. Data Acquisition
- **Role:** Preserve source identifiers
- **Action:** Maintain original country codes
- **Output:** Raw data with original identifiers

### 2. Quality Assessment
- **Role:** Identify identifier issues
- **Action:** Detect missing/invalid codes
- **Output:** Quality report with identifier metrics

### 3. Cleaning
- **Role:** Standardize identifiers
- **Action:** Map to ISO-3, validate format
- **Output:** Standardized country codes

### 4. Deduplication
- **Role:** Enforce uniqueness
- **Action:** Remove duplicate (country_code, year) pairs
- **Output:** Unique composite keys

### 5. Documentation
- **Role:** Document identifier system
- **Action:** Describe ISO-3 standard, composite key
- **Output:** This document, data dictionary

---

## Integration with External Systems

### Compatibility

1. **Climate Data Portals:**
   - Most use ISO-3 codes
   - Enables direct integration
   - Supports data merging

2. **Statistical Systems:**
   - World Bank: ISO-3
   - UN Statistics: ISO-3
   - OECD: ISO-3

3. **Research Tools:**
   - R/Python packages support ISO-3
   - GIS tools recognize ISO-3
   - Database systems handle ISO-3

### Example Integration

**Merging with World Bank Data:**
```python
# Both datasets use ISO-3
df_climate = pd.read_csv("temperature_anomalies_clean.csv")
df_worldbank = pd.read_csv("worldbank_gdp.csv")

# Direct merge on country_code
df_merged = df_climate.merge(
    df_worldbank, 
    on="country_code", 
    how="inner"
)
```

---

## Future Considerations

### Potential Enhancements

1. **URI-Based Identifiers:**
   - Could add URIs for countries (e.g., `http://sws.geonames.org/6252001/`)
   - Enables linked data integration
   - Supports semantic web

2. **Version Identifiers:**
   - Add dataset version identifiers
   - Track changes over time
   - Support versioning

3. **Hash-Based Identifiers:**
   - Generate content hashes for records
   - Detect data changes
   - Support integrity checking

### Maintenance

1. **ISO-3 Updates:**
   - Monitor ISO standard changes
   - Update mappings as needed
   - Document version used

2. **Code Validation:**
   - Regular validation against ISO registry
   - Update invalid codes
   - Maintain quality

---

## References

- International Organization for Standardization. (2020). *ISO 3166-1:2020 - Codes for the representation of names of countries and their subdivisions - Part 1: Country codes*.
- Library of Congress. (n.d.). *MARC Code List for Countries*. https://www.loc.gov/marc/countries/
- United Nations Statistics Division. (n.d.). *Standard Country or Area Codes for Statistical Use (M49)*. https://unstats.un.org/unsd/tradekb/knowledgebase/country-code

---

## Conclusion

Our identifier system design prioritizes:

1. **Standards Compliance:** ISO-3 for international recognition
2. **Uniqueness:** Composite keys for reliable identification
3. **Stability:** Persistent identifiers over time
4. **Interoperability:** Compatibility with other datasets
5. **Efficiency:** Compact yet meaningful identifiers

This approach ensures our dataset can be reliably identified, integrated, and used in climate change research and analysis.

