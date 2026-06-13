"""
StoreBoost AI - Router Tests
===============================
Tests for API routers.
"""
import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    """Set mock environment variables."""
    monkeypatch.setenv("NVIDIA_API_KEY", "test-key-not-real")
    monkeypatch.setenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    monkeypatch.setenv("AI_MODEL", "deepseek-ai/deepseek-v4-pro")
    monkeypatch.setenv("AI_REQUEST_TIMEOUT", "5.0")


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def app():
    """Create FastAPI app."""
    # Clear cached settings so env vars take effect
    from config import get_settings
    get_settings.cache_clear()

    from main import app as fastapi_app
    return fastapi_app


@pytest.fixture
def client(app):
    """Create test client."""
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


def make_mock_llm_response(content: str):
    """Create a mock NVIDIA API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": content}}]
    }
    return mock_response


# ── Health Router Tests ─────────────────────────────────────────────────


@pytest.mark.anyio
async def test_health_endpoint(client):
    """Test /health returns status ok."""
    async with client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "model" in data


# ── Content Router Tests ────────────────────────────────────────────────


@pytest.mark.anyio
async def test_generate_content_success(client):
    """Test /generate-content with mocked AI response."""
    mock_resp = make_mock_llm_response('[{"day": 1, "content_type": "种草"}]')

    with patch("services.ai_service.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        # Clear cached service
        from services.ai_service import get_ai_service
        get_ai_service.cache_clear()

        async with client:
            resp = await client.post(
                "/generate-content",
                json={
                    "shop_id": 1,
                    "shop_name": "Test Shop",
                    "category": "restaurant",
                },
            )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


@pytest.mark.anyio
async def test_generate_content_validation_error(client):
    """Test /generate-content with invalid data."""
    async with client:
        resp = await client.post("/generate-content", json={})
    assert resp.status_code == 422


# ── Review Router Tests ─────────────────────────────────────────────────


@pytest.mark.anyio
async def test_generate_review_reply_success(client):
    """Test /generate-review-reply with mocked AI response."""
    mock_resp = make_mock_llm_response('{"version_a": {"reply": "test reply"}}')

    with patch("services.ai_service.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        from services.ai_service import get_ai_service
        get_ai_service.cache_clear()

        async with client:
            resp = await client.post(
                "/generate-review-reply",
                json={
                    "platform": "dianping",
                    "rating": 2,
                    "content": "Bad food and service",
                    "category": "restaurant",
                    "shop_name": "Test Shop",
                },
            )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


@pytest.mark.anyio
async def test_generate_review_reply_validation_error(client):
    """Test /generate-review-reply with invalid data."""
    async with client:
        resp = await client.post(
            "/generate-review-reply",
            json={"platform": "dianping"},
        )
    assert resp.status_code == 422


# ── Viral Router Tests ──────────────────────────────────────────────────


@pytest.mark.anyio
async def test_generate_viral_title_success(client):
    """Test /generate-viral-title with mocked AI response."""
    mock_resp = make_mock_llm_response('{"titles": ["Title 1", "Title 2"], "best_pick": "Title 1", "reason": "test"}')

    with patch("services.ai_service.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        from services.ai_service import get_ai_service
        get_ai_service.cache_clear()

        async with client:
            resp = await client.post(
                "/generate-viral-title",
                json={
                    "original_title": "Test Title",
                    "category": "restaurant",
                    "shop_name": "Test Shop",
                },
            )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


@pytest.mark.anyio
async def test_generate_viral_title_validation_error(client):
    """Test /generate-viral-title with invalid data."""
    async with client:
        resp = await client.post("/generate-viral-title", json={})
    assert resp.status_code == 422


# ── Growth Router Tests ─────────────────────────────────────────────────


@pytest.mark.anyio
async def test_generate_growth_plan_success(client):
    """Test /generate-growth-plan with mocked AI response."""
    mock_resp = make_mock_llm_response('{"summary": "test summary", "strengths": ["s1"], "weaknesses": ["w1"], "top3_actions": [], "content_suggestion": "test"}')

    with patch("services.ai_service.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        from services.ai_service import get_ai_service
        get_ai_service.cache_clear()

        async with client:
            resp = await client.post(
                "/generate-growth-plan",
                json={
                    "shop_id": 1,
                    "traffic_data": {"avg_rate": 25.0},
                    "content_data": {"published": 5},
                    "review_data": {"negative": 2},
                    "shop_info": {"name": "Test"},
                },
            )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


@pytest.mark.anyio
async def test_generate_growth_plan_validation_error(client):
    """Test /generate-growth-plan with invalid data."""
    async with client:
        resp = await client.post(
            "/generate-growth-plan",
            json={"shop_id": 1},
        )
    assert resp.status_code == 422


# ── OpenAPI Documentation Tests ─────────────────────────────────────────


@pytest.mark.anyio
async def test_openapi_docs_available(client):
    """Test that OpenAPI docs are accessible."""
    async with client:
        resp = await client.get("/docs")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_redoc_available(client):
    """Test that ReDoc is accessible."""
    async with client:
        resp = await client.get("/redoc")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_openapi_json(client):
    """Test that OpenAPI JSON schema is accessible."""
    async with client:
        resp = await client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.json()
    assert "paths" in data
    assert "/health" in data["paths"]
    assert "/generate-content" in data["paths"]
    assert "/generate-review-reply" in data["paths"]
    assert "/generate-viral-title" in data["paths"]
    assert "/generate-growth-plan" in data["paths"]
