"""
StoreBoost AI - Pydantic Model Tests
======================================
Tests for request/response models with validation.
"""
import os
import pytest
from pydantic import ValidationError

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def setup_path():
    """Add ai-service to path."""
    import sys
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "ai-service"))
    yield
    sys.path.pop(0)


class TestGenerateContentRequest:
    """Test GenerateContentRequest model."""

    def test_valid_request(self):
        """Test valid request creation."""
        from models import GenerateContentRequest

        req = GenerateContentRequest(
            shop_id=1,
            shop_name="Test Shop",
            category="restaurant",
            address="123 Street",
            description="A test shop",
            days=7,
        )
        assert req.shop_id == 1
        assert req.shop_name == "Test Shop"
        assert req.days == 7

    def test_default_values(self):
        """Test default values for optional fields."""
        from models import GenerateContentRequest

        req = GenerateContentRequest(
            shop_id=1,
            shop_name="Test Shop",
            category="restaurant",
        )
        assert req.address == ""
        assert req.description == ""
        assert req.days == 7

    def test_invalid_shop_id(self):
        """Test validation for invalid shop_id."""
        from models import GenerateContentRequest

        with pytest.raises(ValidationError):
            GenerateContentRequest(
                shop_id=0,
                shop_name="Test Shop",
                category="restaurant",
            )

    def test_invalid_shop_name_characters(self):
        """Test validation for invalid shop name characters."""
        from models import GenerateContentRequest

        with pytest.raises(ValidationError):
            GenerateContentRequest(
                shop_id=1,
                shop_name="Test <Shop>",
                category="restaurant",
            )

    def test_shop_name_too_long(self):
        """Test validation for shop name too long."""
        from models import GenerateContentRequest

        with pytest.raises(ValidationError):
            GenerateContentRequest(
                shop_id=1,
                shop_name="A" * 101,
                category="restaurant",
            )

    def test_days_out_of_range(self):
        """Test validation for days out of range."""
        from models import GenerateContentRequest

        with pytest.raises(ValidationError):
            GenerateContentRequest(
                shop_id=1,
                shop_name="Test Shop",
                category="restaurant",
                days=31,
            )


class TestGenerateReviewReplyRequest:
    """Test GenerateReviewReplyRequest model."""

    def test_valid_request(self):
        """Test valid request creation."""
        from models import GenerateReviewReplyRequest

        req = GenerateReviewReplyRequest(
            platform="dianping",
            rating=2,
            content="Long wait time, cold food",
            category="restaurant",
            shop_name="Test Shop",
        )
        assert req.rating == 2
        assert req.platform == "dianping"

    def test_invalid_rating(self):
        """Test validation for invalid rating."""
        from models import GenerateReviewReplyRequest

        with pytest.raises(ValidationError):
            GenerateReviewReplyRequest(
                platform="dianping",
                rating=6,
                content="Test content here",
                category="restaurant",
                shop_name="Test Shop",
            )

    def test_content_too_short(self):
        """Test validation for content too short."""
        from models import GenerateReviewReplyRequest

        with pytest.raises(ValidationError):
            GenerateReviewReplyRequest(
                platform="dianping",
                rating=2,
                content="Bad",
                category="restaurant",
                shop_name="Test Shop",
            )


class TestGenerateViralTitleRequest:
    """Test GenerateViralTitleRequest model."""

    def test_valid_request(self):
        """Test valid request creation."""
        from models import GenerateViralTitleRequest

        req = GenerateViralTitleRequest(
            original_title="Test Title",
            category="restaurant",
            shop_name="Test Shop",
        )
        assert req.original_title == "Test Title"


class TestGenerateGrowthPlanRequest:
    """Test GenerateGrowthPlanRequest model."""

    def test_valid_request(self):
        """Test valid request creation."""
        from models import GenerateGrowthPlanRequest

        req = GenerateGrowthPlanRequest(
            shop_id=1,
            traffic_data={"avg_rate": 25.0},
            content_data={"published": 5},
            review_data={"negative": 2},
            shop_info={"name": "Test"},
        )
        assert req.shop_id == 1
        assert req.traffic_data == {"avg_rate": 25.0}


class TestResponseModels:
    """Test response models."""

    def test_health_response(self):
        """Test HealthResponse model."""
        from models import HealthResponse

        resp = HealthResponse(model="test-model")
        assert resp.status == "ok"
        assert resp.version == "1.2.0"

    def test_ai_response(self):
        """Test AIResponse model."""
        from models import AIResponse

        resp = AIResponse(success=True, data={"key": "value"})
        assert resp.success is True
        assert resp.data == {"key": "value"}

    def test_error_response(self):
        """Test ErrorResponse model."""
        from models import ErrorResponse

        resp = ErrorResponse(error="Test error", status_code=500)
        assert resp.error == "Test error"
        assert resp.status_code == 500
