"""
StoreBoost AI - Configuration Management
==========================================
Centralized configuration using Pydantic Settings.
"""
import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # NVIDIA API Configuration
    nvidia_base_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        description="NVIDIA NIM API base URL",
    )
    nvidia_api_key: str = Field(
        default="",
        description="NVIDIA API key for authentication",
    )
    ai_model: str = Field(
        default="deepseek-ai/deepseek-v4-pro",
        description="AI model to use for generation",
    )
    ai_request_timeout: float = Field(
        default=120.0,
        description="Request timeout in seconds",
    )

    # Application Configuration
    app_host: str = Field(default="0.0.0.0", description="Application host")
    app_port: int = Field(default=8000, description="Application port")
    app_debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    # Rate Limiting
    rate_limit_per_minute: int = Field(
        default=60,
        description="API rate limit per minute per IP",
    )

    # Cache Configuration
    cache_ttl_seconds: int = Field(
        default=3600,
        description="Cache TTL in seconds",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


def get_nvidia_api_key() -> str:
    """Get NVIDIA API key with validation."""
    settings = get_settings()
    if not settings.nvidia_api_key:
        raise ValueError("NVIDIA_API_KEY environment variable is required")
    return settings.nvidia_api_key
