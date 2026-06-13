"""
StoreBoost AI - Pytest Configuration
=====================================
Shared fixtures and configuration for all tests.
"""
import os
import sys
import pytest

# Add project root and ai-service to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_SERVICE_DIR = os.path.join(PROJECT_ROOT, "ai-service")

# Ensure ai-service is on the path for imports like `from config import ...`
if AI_SERVICE_DIR not in sys.path:
    sys.path.insert(0, AI_SERVICE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def project_root():
    """Return the absolute path to the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def ai_service_dir():
    """Return the absolute path to the ai-service directory."""
    return AI_SERVICE_DIR


@pytest.fixture
def sample_store_data():
    """Sample store data for testing."""
    return {
        "shop_id": 1,
        "shop_name": "Test Restaurant",
        "category": "restaurant",
        "address": "123 Test Street",
        "description": "A test restaurant for unit testing",
    }


@pytest.fixture
def sample_review_data():
    """Sample review data for testing."""
    return {
        "platform": "dianping",
        "rating": 2,
        "content": "Long wait time, cold food",
        "category": "restaurant",
        "shop_name": "Test Restaurant",
    }


@pytest.fixture
def sample_traffic_data():
    """Sample traffic data for testing."""
    return [
        {"date": "2026-05-22", "total_passers": 320, "total_enter": 85, "enter_rate": 26.56},
        {"date": "2026-05-23", "total_passers": 380, "total_enter": 102, "enter_rate": 26.84},
        {"date": "2026-05-24", "total_passers": 290, "total_enter": 78, "enter_rate": 26.90},
        {"date": "2026-05-25", "total_passers": 410, "total_enter": 115, "enter_rate": 28.05},
        {"date": "2026-05-26", "total_passers": 450, "total_enter": 128, "enter_rate": 28.44},
        {"date": "2026-05-27", "total_passers": 520, "total_enter": 148, "enter_rate": 28.46},
        {"date": "2026-05-28", "total_passers": 480, "total_enter": 136, "enter_rate": 28.33},
    ]
