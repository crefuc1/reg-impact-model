import duckdb

# Public OWID CO2 dataset (CSV). One row per location-year.
CSV_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

con = duckdb.connect()

# DuckDB may need the httpfs extension to read HTTPS in some environments.
# Try loading it; if it isn't needed, it won't hurt.
try:
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
except Exception as e:
    print("Note: httpfs install/load skipped or failed (may still work):", e)

# Get the last 5 years of data for a single "location" (choose 'World' for simplicity).
# co2 column is typically in million tonnes (MtCO2) in OWID.
query = f"""
SELECT
  year,
  co2
FROM read_csv_auto('{CSV_URL}')
WHERE country = 'World'
  AND co2 IS NOT NULL
ORDER BY year DESC
LIMIT 5
"""

df = con.execute(query).df().sort_values("year")
print(df.to_string(index=False))
