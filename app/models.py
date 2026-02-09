from pydantic import BaseModel, Field
from typing import List

class NPVFromSQLRequest(BaseModel):
    country: str = Field(
        "World",
        description="OWID country name (e.g., 'World', 'United States')"
    )
    n_years: int = Field(
        5,
        ge=1,
        le=20,
        description="Number of most recent years to use"
    )
    discount_rate: float = Field(
        0.05,
        ge=-0.99,
        description="Discount rate (e.g., 0.05)"
    )
    reduction_rate: float = Field(
        0.02,
        ge=0.0,
        le=1.0,
        description="Fractional emissions reduction attributed to regulation"
    )
    value_per_mtco2: float = Field(
        10_000_000,
        ge=0.0,
        description="Dollar value per MtCO2 (exercise parameter)"
    )
    annual_cost: float = Field(
        300_000_000,
        ge=0.0,
        description="Annual regulatory cost in dollars"
    )
