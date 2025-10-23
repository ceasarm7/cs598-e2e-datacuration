import pandas as pd

# Assume the raw data is loaded
df = pd.read_csv('raw_temperature_anomalies.csv')

print(f"Original shape: {df.shape}")

# --- Cleaning Step 1: Deduplication ---
# Identify and remove repeated records for the same country and year [cite: 63, 80]
initial_duplicates = df.duplicated(subset=['country', 'year']).sum()
df_cleaned = df.drop_duplicates(subset=['country', 'year'], keep='first')
print(f"Duplicates removed: {initial_duplicates}")
print(f"Shape after deduplication: {df_cleaned.shape}")

# --- Cleaning Step 2: Country Code Standardization (Addressing Missing/Inconsistent Codes) ---
# Simple standardization/filling example (This would be more complex in reality)
def standardize_country_codes(df):
    # Example mapping for missing/inconsistent codes (based on manual check)
    mapping = {
        'UK': 'GBR',
        'USA': 'USA'  # Assuming a standard is needed, even if correct
    }
    # Apply mapping only if country_code is short or known to be inconsistent
    for key, value in mapping.items():
        df.loc[df['country'] == key, 'country_code'] = value
    
    # Fill remaining NULL country_code entries (e.g., using a lookup table if available)
    # For now, we flag the remaining missing codes for manual review
    df['country_code'] = df['country_code'].fillna('MISSING')
    return df

df_cleaned = standardize_country_codes(df_cleaned)
print(f"Missing Country Codes after standardization: {df_cleaned['country_code'].eq('MISSING').sum()}")

# --- Next Steps (Planned for final team delivery) ---
# Outlier detection and flagging using statistical methods [cite: 67, 83]
# Handling Missing Temperature Anomalies (e.g., interpolation or regional mean) [cite: 80, 83]

# df_cleaned.to_csv('cleaned_temperature_anomalies_step1.csv', index=False)
