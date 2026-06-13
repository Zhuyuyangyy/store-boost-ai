"""
StoreBoost AI - Configuration Tests
=====================================
Tests for configuration management.
"""
import os
import pytest
from unittest.mock import patch


class TestSettings:
    """Test Settings class from config module."""

    def test_settings_default_values(self):
        """Test that settings have correct default values."""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai-service"))
        from config import Settings

        with patch.dict(os.environ, {"NVIDIA_API_KEY": "test-key"}, clear=True):
            settings = Settings()
            assert settings.nvidia_base_url == "https://integrate.api.nvidia.com/v1"
            assert settings.ai_model == "deepseek-ai/deepseek-v4-pro"
            assert settings.ai_request_timeout == 120.0
            assert settings.app_port == 8000
            assert settings.log_level == "INFO"

    def test_settings_from_env(self):
        """Test that settings can be loaded from environment variables."""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai-service"))
        from config import Settings

        env_vars = {
            "NVIDIA_API_KEY": "custom-key",
            "AI_MODEL": "custom-model",
            "APP_PORT": "9000",
            "LOG_LEVEL": "DEBUG",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.nvidia_api_key == "custom-key"
            assert settings.ai_model == "custom-model"
            assert settings.app_port == 9000
            assert settings.log_level == "DEBUG"

    def test_get_settings_cached(self):
        """Test that get_settings returns cached instance."""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai-service"))
        from config import get_settings

        # Clear cache
        get_settings.cache_clear()

        with patch.dict(os.environ, {"NVIDIA_API_KEY": "test-key"}, clear=True):
            settings1 = get_settings()
            settings2 = get_settings()
            assert settings1 is settings2

    def test_get_nvidia_api_key_raises_without_key(self):
        """Test that get_nvidia_api_key raises without API key."""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai-service"))
        from config import get_nvidia_api_key, get_settings

        # Clear cache
        get_settings.cache_clear()

        with patch.dict(os.environ, {"NVIDIA_API_KEY": ""}, clear=True):
            with pytest.raises(ValueError, match="NVIDIA_API_KEY"):
                get_nvidia_api_key()

    def test_get_nvidia_api_key_returns_key(self):
        """Test that get_nvidia_api_key returns the API key."""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai-service"))
        from config import get_nvidia_api_key, get_settings

        # Clear cache
        get_settings.cache_clear()

        with patch.dict(os.environ, {"NVIDIA_API_KEY": "test-key-123"}, clear=True):
            key = get_nvidia_api_key()
            assert key == "test-key-123"
