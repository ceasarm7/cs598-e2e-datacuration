-- Schema for the Annual Temperature Anomalies dataset
-- Based on entities identified in Phase I Report
CREATE TABLE TemperatureAnomalies (
    country VARCHAR(100),              -- Represents the geographical area or country [cite: 19, 31]
    country_code VARCHAR(3),           -- A 3-letter code representing the country [cite: 20, 32]
    year INT,                          -- The year for which the temperature anomaly is recorded [cite: 20, 33]
    temperature_anomaly DECIMAL(7,6),  -- Deviation of temperature from a baseline reference temperature, measured in °C [cite: 21, 34]
    -- Future columns for data integration or derived values could be added here.
    PRIMARY KEY (country_code, year)
);