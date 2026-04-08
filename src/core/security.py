from fastapi import Header, HTTPException
from typing import Optional
import httpx
from src.core.config import settings


async def get_current_tenant(
    x_tenant_id: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None),
):
    if not x_tenant_id and not authorization:
        raise HTTPException(status_code=401, detail="Missing tenant context")

    if authorization:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.AUTH_SERVICE_URL}/validate",
                    headers={"Authorization": authorization},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json().get("tenant_id")
            except Exception:
                pass

    return x_tenant_id
