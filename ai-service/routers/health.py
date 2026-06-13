"""
StoreBoost AI - Health Router
===============================
Health check endpoints.
"""
from fastapi import APIRouter

from config import get_settings
from models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check service health status.

    Returns:
        HealthResponse with status and model info
    """
    settings = get_settings()
    return HealthResponse(
        status="ok",
        model=settings.ai_model,
    )
