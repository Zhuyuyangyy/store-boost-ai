"""
StoreBoost AI - API Integration Tests
======================================
Tests for the FastAPI AI service endpoints using httpx test client.
Run: pytest tests/test_api.py -v
"""
import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

httpx = pytest.importorskip("httpx")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    """Set mock environment variables for AI service."""
    monkeypatch.setenv("NVIDIA_API_KEY", "test-key-not-real")
    monkeypatch.setenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    monkeypatch.setenv("AI_MODEL", "deepseek-ai/deepseek-v4-pro")
    monkeypatch.setenv("AI_REQUEST_TIMEOUT", "5.0")


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def app():
    """Import the FastAPI app."""
    from main import app as fastapi_app
    return fastapi_app


@pytest.fixture
def client(app):
    """Create a test client for the FastAPI app."""
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# ── Health Endpoint Tests ────────────────────────────────────────────────

@pytest.mark.anyio
async def test_health_endpoint(client):
    """Test /health returns status ok."""
    async with client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "model" in data


# ── Request Model Validation Tests ──────────────────────────────────────

@pytest.mark.anyio
async def test_generate_content_missing_fields(client):
    """Test /generate-content rejects incomplete requests."""
    async with client:
        resp = await client.post("/generate-content", json={})
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_generate_review_reply_missing_fields(client):
    """Test /generate-review-reply rejects incomplete requests."""
    async with client:
        resp = await client.post("/generate-review-reply", json={"platform": "dianping"})
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_generate_viral_title_missing_fields(client):
    """Test /generate-viral-title rejects incomplete requests."""
    async with client:
        resp = await client.post("/generate-viral-title", json={})
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_generate_growth_plan_missing_fields(client):
    """Test /generate-growth-plan rejects incomplete requests."""
    async with client:
        resp = await client.post("/generate-growth-plan", json={"shop_id": 1})
    assert resp.status_code == 422


# ── Request Model Valid Payload Tests ───────────────────────────────────

def test_content_request_model():
    """Test GenerateContentRequest accepts valid data."""
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


def test_review_reply_request_model():
    """Test GenerateReviewReplyRequest accepts valid data."""
    from models import GenerateReviewReplyRequest

    req = GenerateReviewReplyRequest(
        platform="dianping",
        rating=2,
        content="Bad food",
        category="restaurant",
        shop_name="Test Shop",
    )
    assert req.rating == 2
    assert req.platform == "dianping"


def test_viral_title_request_model():
    """Test GenerateViralTitleRequest accepts valid data."""
    from models import GenerateViralTitleRequest

    req = GenerateViralTitleRequest(
        original_title="Test Title",
        category="restaurant",
        shop_name="Test Shop",
    )
    assert req.original_title == "Test Title"


def test_growth_plan_request_model():
    """Test GenerateGrowthPlanRequest accepts valid data."""
    from models import GenerateGrowthPlanRequest

    req = GenerateGrowthPlanRequest(
        shop_id=1,
        traffic_data={"avg_rate": 25.0},
        content_data={"published": 5},
        review_data={"negative": 2},
        shop_info={"name": "Test", "category": "restaurant"},
    )
    assert req.shop_id == 1
    assert req.traffic_data == {"avg_rate": 25.0}


# ── Response Parsing Tests ──────────────────────────────────────────────

def test_build_response_with_valid_json():
    """Test build_response parses valid JSON from AI output."""
    from services.ai_service import AIService

    service = AIService(
        api_key="test",
        base_url="https://test.com",
        model="test",
        timeout=5.0,
    )
    raw = '{"key": "value"}'
    result = service.build_response(raw)
    assert result["success"] is True
    assert result["data"] == {"key": "value"}


def test_build_response_with_markdown_json():
    """Test build_response parses markdown-wrapped JSON."""
    from services.ai_service import AIService

    service = AIService(
        api_key="test",
        base_url="https://test.com",
        model="test",
        timeout=5.0,
    )
    raw = '```json\n{"key": "value"}\n```'
    result = service.build_response(raw)
    assert result["success"] is True
    assert result["data"] == {"key": "value"}


def test_build_response_with_fallback():
    """Test build_response uses fallback when JSON parsing fails."""
    from services.ai_service import AIService

    service = AIService(
        api_key="test",
        base_url="https://test.com",
        model="test",
        timeout=5.0,
    )
    raw = "This is not JSON at all"
    fallback = {"summary": "fallback data"}
    result = service.build_response(raw, fallback_data=fallback)
    assert result["success"] is True
    assert result["data"] == fallback


def test_build_response_no_json_no_fallback():
    """Test build_response raises when no JSON and no fallback."""
    from services.ai_service import AIService
    from fastapi import HTTPException

    service = AIService(
        api_key="test",
        base_url="https://test.com",
        model="test",
        timeout=5.0,
    )
    raw = "This is not JSON"
    with pytest.raises(HTTPException) as exc_info:
        service.build_response(raw)
    assert exc_info.value.status_code == 500
