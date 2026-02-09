from dataclasses import dataclass
from typing import Dict, Sequence

@dataclass
class BenefitCostAnalysis:
    def present_value(self, value: float, discount_rate: float, year_index: int) -> float:
        # year_index is 1..N
        return float(value) / ((1.0 + float(discount_rate)) ** int(year_index))

    def calculate_net_present_value(
        self,
        benefits: Sequence[float],
        costs: Sequence[float],
        discount_rate: float,
    ) -> Dict[str, float]:
        if len(benefits) != len(costs):
            raise ValueError("benefits and costs must be same length")

        pv_b = [self.present_value(b, discount_rate, i + 1) for i, b in enumerate(benefits)]
        pv_c = [self.present_value(c, discount_rate, i + 1) for i, c in enumerate(costs)]

        total_pv_b = sum(pv_b)
        total_pv_c = sum(pv_c)
        npv = total_pv_b - total_pv_c
        bcr = (total_pv_b / total_pv_c) if total_pv_c != 0 else float("inf")

        return {
            "total_pv_benefits": float(total_pv_b),
            "total_pv_costs": float(total_pv_c),
            "npv": float(npv),
            "benefit_cost_ratio": float(bcr),
        }
