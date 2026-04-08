"""
Dashboard summary routes
"""
from fastapi import APIRouter, Depends, HTTPException
import logging
from src.schemas.summary import DashboardSummary
from src.services.analytics_client import AnalyticsClient
from src.core.security import get_current_tenant

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary(
    tenant_id: str = Depends(get_current_tenant)
):
    """
    Get dashboard summary metrics for a tenant.
    Requires X-Tenant-ID header.
    """
    logger.info(f"Dashboard summary requested for tenant: {tenant_id}")
    
    client = AnalyticsClient()
    try:
        summary = await client.get_summary(tenant_id)
        logger.info(f"Summary retrieved successfully")
        return summary
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting summary: {str(e)}")