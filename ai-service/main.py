"""
StoreBoost AI Service - FastAPI AI Layer
Port: 8000
Called by Spring Boot backend, invokes NVIDIA NIM API.

Refactored: Modular architecture with separated concerns.
"""
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from config import get_settings
from routers import (
    health_router,
    content_router,
    review_router,
    viral_router,
    growth_router,
)


# ── Logging Setup ───────────────────────────────────────────────────────


def setup_logging(level: str = "INFO") -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# ── Lifespan Events ────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    settings = get_settings()
    setup_logging(settings.log_level)
    logger = logging.getLogger("storeboost-ai")
    logger.info(
        "StoreBoost AI Service starting | model=%s | port=%d",
        settings.ai_model,
        settings.app_port,
    )
    yield
    logger.info("StoreBoost AI Service shutting down")


# ── FastAPI Application ────────────────────────────────────────────────


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="StoreBoost AI Service",
        description="AI content generation service for offline stores",
        version="1.2.0",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(content_router)
    app.include_router(review_router)
    app.include_router(viral_router)
    app.include_router(growth_router)

    return app


# ── Application Instance ───────────────────────────────────────────────

app = create_app()


# ── Entry Point ────────────────────────────────────────────────────────


def run_server() -> None:
    """Run the application server."""
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run_server()
