import duckdb
from typing import Dict, List, Tuple

OWID_CSV_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

def _get_duckdb_connection():
    con = duckdb.connect()
    try:
        con.execute("INSTALL httpfs;")
        con.execute("LOAD httpfs;")
    except Exception:
        pass
    return con

def fetch_last_n_years_co2(country: str, n_years: int = 5) -> List[Tuple[int, float]]:
    """
    Returns [(year, co2_mt)] for the last n_years available for the given country.
    """
    con = _get_duckdb_connection()

    query = """
    SELECT year, co2
    FROM read_csv_auto(?)
    WHERE country = ?
      AND co2 IS NOT NULL
    ORDER BY year DESC
    LIMIT ?
    """

    df = con.execute(query, [OWID_CSV_URL, country, n_years]).df().sort_values("year")
    return list(zip(df["year"].astype(int), df["co2"].astype(float)))

def build_streams_from_co2(
    year_co2: List[Tuple[int, float]],
    reduction_rate: float,
    value_per_mtco2: float,
    annual_cost: float,
) -> Dict[str, List[float]]:
    years = [y for y, _ in year_co2]
    co2 = [v for _, v in year_co2]

    benefits = [(x * reduction_rate) * value_per_mtco2 for x in co2]
    costs = [annual_cost for _ in years]

    return {
        "years": years,
        "baseline_co2_mt": co2,
        "benefits": benefits,
        "costs": costs,
    }
