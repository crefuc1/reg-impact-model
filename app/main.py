from fastapi import FastAPI
from app.bca import BenefitCostAnalysis
from app.models import NPVFromSQLRequest
from app.sql_bca import fetch_last_n_years_co2, build_streams_from_co2

app = FastAPI(title="Reg Impact Model (SQL -> NPV)")

bca = BenefitCostAnalysis()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/bca/npv-from-sql")
def npv_from_sql(req: NPVFromSQLRequest):
    year_co2 = fetch_last_n_years_co2(req.country, req.n_years)

    streams = build_streams_from_co2(
        year_co2=year_co2,
        reduction_rate=req.reduction_rate,
        value_per_mtco2=req.value_per_mtco2,
        annual_cost=req.annual_cost,
    )

    result = bca.calculate_net_present_value(
        benefits=streams["benefits"],
        costs=streams["costs"],
        discount_rate=req.discount_rate,
    )

    return {
        "inputs": req.model_dump(),
        "years": streams["years"],
        "baseline_co2_mt": streams["baseline_co2_mt"],
        "benefits": streams["benefits"],
        "costs": streams["costs"],
        **result,
    }

