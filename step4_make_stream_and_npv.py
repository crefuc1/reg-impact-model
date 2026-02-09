import duckdb

CSV_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

# ---- Changeable inputs (exercise knobs) ----
discount_rate = 0.05          # 5%
reduction_rate = 0.02         # 2% emissions reduction attributed to regulation
value_per_mtco2 = 10_000_000  # $ per MtCO2 (toy value for exercise)
annual_cost = 300_000_000     # $ per year (toy value for exercise)

con = duckdb.connect()

try:
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
except Exception:
    pass

# Pull last 5 years baseline emissions (World)
baseline = con.execute(f"""
    SELECT year, co2
    FROM read_csv_auto('{CSV_URL}')
    WHERE country = 'World' AND co2 IS NOT NULL
    ORDER BY year DESC
    LIMIT 5
""").df().sort_values("year")

years = baseline["year"].tolist()
co2 = baseline["co2"].tolist()

# Build benefit & cost streams
benefits = [(x * reduction_rate) * value_per_mtco2 for x in co2]
costs = [annual_cost for _ in years]

# Discount to PV and compute NPV
pv_b = [b / ((1 + discount_rate) ** (i + 1)) for i, b in enumerate(benefits)]
pv_c = [c / ((1 + discount_rate) ** (i + 1)) for i, c in enumerate(costs)]
npv = sum(pv_b) - sum(pv_c)

print("Years:", years)
print("Baseline CO2 (MtCO2):", [round(x, 3) for x in co2])
print("Benefits ($):", [round(x, 2) for x in benefits])
print("Costs ($):", [round(x, 2) for x in costs])
print("PV Benefits ($):", [round(x, 2) for x in pv_b])
print("PV Costs ($):", [round(x, 2) for x in pv_c])
print("NPV ($):", round(npv, 2))
