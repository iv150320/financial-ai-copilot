"""
Health check endpoint — used by load balancers, K8s probes, and
Docker Compose health checks.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.models.pydantic_models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    """Return the current service health status."""
    return HealthResponse(
        status="ok",
        version=settings.VERSION,
    )
