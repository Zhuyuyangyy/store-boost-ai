"""
StoreBoost AI - Service Tests
===============================
Tests for AI service functionality.
"""
import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def setup_path():
    """Add ai-service to path."""
    import sys
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "ai-service"))
    yield
    sys.path.pop(0)


@pytest.fixture
def ai_service():
    """Create AI service instance."""
    from services.ai_service import AIService
    return AIService(
        api_key="test-key",
        base_url="https://integrate.api.nvidia.com/v1",
        model="test-model",
        timeout=5.0,
    )


class TestAIService:
    """Test AIService class."""

    def test_init(self, ai_service):
        """Test service initialization."""
        assert ai_service.api_key == "test-key"
        assert ai_service.model == "test-model"
        assert ai_service.timeout == 5.0

    @pytest.mark.anyio
    async def test_call_llm_success(self, ai_service):
        """Test successful LLM call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"result": "success"}'}}]
        }

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await ai_service.call_llm("test prompt")
            assert result == '{"result": "success"}'

    @pytest.mark.anyio
    async def test_call_llm_timeout(self, ai_service):
        """Test LLM call timeout."""
        import httpx

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.TimeoutException("Timeout")
            with pytest.raises(Exception) as exc_info:
                await ai_service.call_llm("test prompt")
            assert "timeout" in str(exc_info.value).lower() or "504" in str(exc_info.value)

    @pytest.mark.anyio
    async def test_call_llm_api_error(self, ai_service):
        """Test LLM call API error."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            with pytest.raises(Exception) as exc_info:
                await ai_service.call_llm("test prompt")
            assert "502" in str(exc_info.value) or "NVIDIA API error" in str(exc_info.value)

    def test_build_response_valid_json(self, ai_service):
        """Test build_response with valid JSON."""
        raw = '{"key": "value"}'
        result = ai_service.build_response(raw)
        assert result["success"] is True
        assert result["data"] == {"key": "value"}

    def test_build_response_markdown_json(self, ai_service):
        """Test build_response with markdown-wrapped JSON."""
        raw = '```json\n{"key": "value"}\n```'
        result = ai_service.build_response(raw)
        assert result["success"] is True
        assert result["data"] == {"key": "value"}

    def test_build_response_with_fallback(self, ai_service):
        """Test build_response with fallback data."""
        raw = "Not JSON at all"
        fallback = {"summary": "fallback"}
        result = ai_service.build_response(raw, fallback_data=fallback)
        assert result["success"] is True
        assert result["data"] == fallback

    def test_build_response_no_json_no_fallback(self, ai_service):
        """Test build_response raises without JSON and fallback."""
        raw = "Not JSON"
        with pytest.raises(Exception) as exc_info:
            ai_service.build_response(raw)
        assert "500" in str(exc_info.value) or "unparseable" in str(exc_info.value)


class TestGetAIService:
    """Test get_ai_service factory function."""

    def test_get_ai_service_cached(self):
        """Test that get_ai_service returns cached instance."""
        from services.ai_service import get_ai_service
        from config import get_settings

        # Clear caches
        get_ai_service.cache_clear()
        get_settings.cache_clear()

        with patch.dict(os.environ, {"NVIDIA_API_KEY": "test-key"}, clear=True):
            service1 = get_ai_service()
            service2 = get_ai_service()
            assert service1 is service2
