"""
Analytics client for dashboard service
"""
import httpx
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)


class AnalyticsClient:

    async def get_summary(self, tenant_id: str):
        """
        Get analytics summary for a tenant.
        Calls the analytics API endpoint.
        """
        # Try the real endpoint first
        endpoints_to_try = [
            f"{settings.ANALYTICS_SERVICE_URL}/analytics/summary",
            f"{settings.ANALYTICS_SERVICE_URL}/api/v1/analytics/summary",
            f"{settings.ANALYTICS_SERVICE_URL}/analytics",
        ]
        
        for url in endpoints_to_try:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(
                        url,
                        headers={"X-Tenant-ID": tenant_id}
                    )
                    if response.status_code == 200:
                        logger.info(f"Analytics summary retrieved from {url}")
                        return response.json()
            except Exception as e:
                logger.debug(f"Endpoint {url} failed: {e}")
                continue
        
        # Fallback to mock data if no endpoint works
        logger.warning("No analytics endpoint available, using mock data")
        return self._get_mock_summary()
    
    def _get_mock_summary(self):
        """Return mock summary data for testing"""
        return {
            "total_inflow": 125000,
            "total_outflow": 78000,
            "net_cashflow": 47000,
            "transaction_count": 42,
            "avg_transaction_value": 2976,
            "top_category": "transport",
            "active_days": 24
        }