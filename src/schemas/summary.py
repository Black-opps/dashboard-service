from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_inflow: float
    total_outflow: float
    net_cashflow: float
    transaction_count: int
    avg_transaction_value: float
    top_category: str
    active_days: int
