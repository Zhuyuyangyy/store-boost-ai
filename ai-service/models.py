"""
StoreBoost AI - Pydantic Models
=================================
Request and response models with validation.
"""
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ── Request Models ──────────────────────────────────────────────────────


class GenerateContentRequest(BaseModel):
    """Request model for content calendar generation."""

    shop_id: int = Field(..., gt=0, description="Unique shop identifier")
    shop_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the shop",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Business category (e.g., restaurant, retail)",
    )
    address: str = Field(
        default="",
        max_length=200,
        description="Shop address",
    )
    description: str = Field(
        default="",
        max_length=500,
        description="Shop description",
    )
    days: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Number of days to generate content for",
    )

    @field_validator("shop_name")
    @classmethod
    def validate_shop_name(cls, v: str) -> str:
        """Validate shop name doesn't contain special characters."""
        if any(char in v for char in ["<", ">", "{", "}"]):
            raise ValueError("Shop name contains invalid characters")
        return v.strip()


class GenerateReviewReplyRequest(BaseModel):
    """Request model for review reply generation."""

    platform: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Review platform (e.g., dianping, meituan)",
    )
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating from 1 to 5",
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Review content",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Business category",
    )
    shop_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the shop",
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate review content."""
        if len(v.strip()) < 5:
            raise ValueError("Review content must be at least 5 characters")
        return v.strip()


class GenerateViralTitleRequest(BaseModel):
    """Request model for viral title generation."""

    original_title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Original title or topic",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Business category",
    )
    shop_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the shop",
    )


class GenerateGrowthPlanRequest(BaseModel):
    """Request model for growth plan generation."""

    shop_id: int = Field(..., gt=0, description="Unique shop identifier")
    traffic_data: dict[str, Any] = Field(
        ...,
        description="Weekly traffic data",
    )
    content_data: dict[str, Any] = Field(
        ...,
        description="Content publishing data",
    )
    review_data: dict[str, Any] = Field(
        ...,
        description="Review and rating data",
    )
    shop_info: dict[str, Any] = Field(
        ...,
        description="Shop information",
    )


# ── Response Models ─────────────────────────────────────────────────────


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    model: str
    version: str = "1.2.0"


class AIResponse(BaseModel):
    """Standard AI service response."""

    success: bool
    data: Any
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    status_code: int


# ── Internal Models ─────────────────────────────────────────────────────


class NVIDIAAPIPayload(BaseModel):
    """NVIDIA API request payload."""

    model: str
    messages: list[dict[str, str]]
    temperature: float = 0.7
    max_tokens: int = 2048


class NVIDIAAPIResponse(BaseModel):
    """NVIDIA API response model."""

    choices: list[dict[str, Any]]

    def get_content(self) -> str:
        """Extract content from first choice."""
        if not self.choices:
            raise ValueError("No choices in response")
        return self.choices[0].get("message", {}).get("content", "")
