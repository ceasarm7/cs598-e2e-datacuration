# ============================================================
# Climate Change Impacts Data - Temperature Anomalies
# ============================================================

import pandas as pd
from pathlib import Path

# --- Input / Output File Paths ---
INFILE   = "temperature_anomalies_refine_clean_base.csv"   # OpenRefine export
OUT_INIT = "temperature_anomalies_initial_clean.csv"       # initial cleaned snapshot
OUT_DQ   = "temperature_anomalies_initial_dq_report.csv"   # simple QA metrics


# --- Cleaning Step 1: Load and Standardize Column Names ---
# Purpose: Map possible headers to a consistent schema used downstream.
def load_and_standardize_columns(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Accept either OpenRefine-style headers or already-standard ones
    colmap = {
        "Entity": "country",
        "Code": "country_code",
        "Year": "year",
        "Temperature anomaly": "temperature_anomaly",
        "country": "country",
        "country_code": "country_code",
        "year": "year",
        "temperature_anomaly": "temperature_anomaly",
    }

    # Keep only recognized columns; warn if we dropped any
    incoming = list(df.columns)
    keep = [c for c in incoming if c in colmap]
    dropped = [c for c in incoming if c not in colmap]
    if dropped:
        print(f"[WARN] Dropping unrecognized columns: {dropped}")

    df = df[keep].rename(columns={c: colmap[c] for c in keep})

    # Ensure all required columns are present
    required = {"country", "country_code", "year", "temperature_anomaly"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    print(f"[INFO] Loaded {path}. Columns standardized to {sorted(df.columns.tolist())}")
    return df


# --- Cleaning Step 2: Country Code Standardization (Addressing Missing/Inconsistent Codes) ---
# Simple standardization/filling example (This would be more complex in reality)
def standardize_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    df["country_code"] = (
        df["country_code"]
        .astype("string")
        .str.strip()
        .str.upper()
    )
    # Map known short codes / aliases to ISO-3
    code_map = {
        # Short codes and aliases
        "UK": "GBR", "GB": "GBR", "UAE": "ARE", "USA": "USA", "US": "USA",
        "KOREA, REP.": "KOR", "KOREA, REP": "KOR", "S. KOREA": "KOR",
        "KOREA, DEM. PEOPLE’S REP.": "PRK", "N. KOREA": "PRK",
        "RUSSIA": "RUS", "VIET NAM": "VNM", "IRAN (ISLAMIC REPUBLIC OF)": "IRN",
        "SYRIAN ARAB REPUBLIC": "SYR", "BOLIVIA (PLURINATIONAL STATE OF)": "BOL",
        "VENEZUELA, RB": "VEN", "VENEZUELA (BOLIVARIAN REPUBLIC OF)": "VEN",
        "TANZANIA, UNITED REPUBLIC OF": "TZA", "LAO PDR": "LAO",
        "BRUNEI DARUSSALAM": "BRN", "CÔTE D’IVOIRE": "CIV", "COTE D'IVOIRE": "CIV",
        "CONGO, DEM. REP.": "COD", "CONGO, REP.": "COG",
        "CZECHIA": "CZE", "CZECH REPUBLIC": "CZE",
        "ESWATINI": "SWZ", "SWAZILAND": "SWZ",
        "MYANMAR (BURMA)": "MMR", "BURMA": "MMR",
        "PALESTINE": "PSE", "WEST BANK AND GAZA": "PSE",
        "MACEDONIA, FYR": "MKD", "NORTH MACEDONIA": "MKD",
        "MICRONESIA, FEDERATED STATES OF": "FSM",
        "ST. KITTS AND NEVIS": "KNA", "ST. LUCIA": "LCA", "ST. VINCENT AND THE GRENADINES": "VCT"
    }
    df["country_code"] = df["country_code"].replace(code_map)

    # Invalidate anything that doesn't look like ISO-3 (exactly 3 A–Z)
    iso3_mask = df["country_code"].str.fullmatch(r"[A-Z]{3}", na=False)
    invalid_count = (~iso3_mask & df["country_code"].notna()).sum()
    if invalid_count > 0:
        print(f"[WARN] Found {int(invalid_count)} non-ISO-3 codes; setting to NaN for visibility in DQ.")
        df.loc[~iso3_mask, "country_code"] = pd.NA

    return df


# --- Cleaning Step 3: Type Coercion (Numbers & Strings) ---
# Purpose: Ensure numeric operations behave correctly downstream.
def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    df["country"] = df["country"].astype("string").str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["temperature_anomaly"] = pd.to_numeric(df["temperature_anomaly"], errors="coerce")
    return df


# --- Cleaning Step 4: Deduplication (Remove Duplicate Country-Year Records) ---
# Purpose: Keep a single record for each (country_code, year) pair.
def enforce_uniqueness(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    df = df.reset_index(names="__row_ix__")
    df = (
        df.sort_values(["country_code", "year", "__row_ix__"])
          .drop_duplicates(subset=["country_code", "year"], keep="first")
          .drop(columns="__row_ix__")
    )
    removed = before - len(df)
    print(f"[INFO] Deduplication removed {removed} rows (by country_code + year).")
    return df, removed


# --- Cleaning Step 5: Lightweight QA Diagnostics (No Mutation) ---
# Purpose: Produce a tiny DQ report to describe the initial cleaning impact.
def make_initial_dq_report(df: pd.DataFrame, dups_removed: int, rows_input: int) -> pd.DataFrame:
    missing_code = df["country_code"].isna().sum()
    dq = pd.DataFrame({
        "rows_input": [rows_input],
        "rows_after_initial_clean": [len(df)],
        "unique_countries": [df["country_code"].nunique(dropna=True)],
        "years_min": [int(df["year"].min()) if df["year"].notna().any() else None],
        "years_max": [int(df["year"].max()) if df["year"].notna().any() else None],
        "duplicates_removed": [dups_removed],
        "missing_country": [int(df["country"].isna().sum())],
        "missing_country_code_or_invalid": [int(missing_code)],
        "missing_year": [int(df["year"].isna().sum())],
        "missing_temperature_anomaly": [int(df["temperature_anomaly"].isna().sum())],
    })
    return dq


# --- Main (Initial Steps Only) ---
def main():
    assert Path(INFILE).exists(), f"Input file not found: {INFILE}"

    # Step 1: load + standardize headers
    df = load_and_standardize_columns(INFILE)
    rows_input = len(df)

    # Step 2: light country-code standardization
    df = standardize_country_codes(df)

    # Step 3: type coercion
    df = coerce_types(df)

    # Step 4: deduplicate on (country_code, year)
    df, dups_removed = enforce_uniqueness(df)

    # Step 5: QA diagnostics (no outlier changes, no imputation)
    dq = make_initial_dq_report(df, dups_removed, rows_input)

    # Save initial snapshot + DQ report
    df = df.sort_values(["country_code", "year"]).reset_index(drop=True)
    df.to_csv(OUT_INIT, index=False)
    dq.to_csv(OUT_DQ, index=False)

    print(f"[INFO] Initial cleaning complete. Saved:\n - {OUT_INIT}\n - {OUT_DQ}")


if __name__ == "__main__":
    main()


# ============================================================
# Next Steps for Final Submission
# ============================================================
# [ ] Implement statistical outlier handling per country (compute z-scores)
# [ ] Apply conservative winsorization or strict NaN replacement for |z| > 3
# [ ] Perform per-country linear interpolation for missing values (by year)
# [ ] Forward/backward fill edge cases only when justified
# [ ] Add reproducibility features (CLI args, config, or workflow script)
# [ ] Export a comprehensive DQ report summarizing outliers + imputation
# [ ] Create DataCite-style metadata JSON and data dictionary
# [ ] Describe provenance and workflow (OpenRefine → Python → Outputs)
# [ ] Package final artifacts:
#       - temperature_anomalies_clean_final.csv
#       - temperature_anomalies_dq_report.csv
#       - final_cleaning_script.py (automated workflow)
# [ ] Ensure all documentation aligns with course requirements for:
#       • Data Lifecycle (M1)
#       • Metadata & Provenance (M8, M12)
#       • Reproducibility & Transparency
#       • Ethical/legal constraints & licensing (CC BY 4.0)
#       • Dissemination (GitHub or ZIP-ready structure)
