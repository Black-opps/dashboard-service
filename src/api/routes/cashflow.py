from fastapi import APIRouter, Depends, Query
from src.core.security import get_current_tenant

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/cashflow")
async def cashflow_trend(
    days: int = Query(30, ge=1, le=365),
    tenant_id: str = Depends(get_current_tenant)
):
    # TODO: Connect to cashflow-analyzer service
    return [
        {"date": "2026-04-01", "inflow": 5000, "outflow": 3200},
        {"date": "2026-04-02", "inflow": 4500, "outflow": 2800}
    ]
