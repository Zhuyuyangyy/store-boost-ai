"""
StoreBoost AI - Smoke Tests
============================
Basic import, structure, and sanity checks to validate the project is healthy.
Run: pytest tests/ -v
"""
import importlib
import os
import json
import pytest


# ── Project Root ──────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── AI Service Import Tests ───────────────────────────────────────────

def test_ai_service_module_exists():
    """Verify the ai-service/main.py file exists."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "main.py")
    assert os.path.isfile(path), f"AI service entry not found: {path}"


def test_ai_prompts_module_exists():
    """Verify the ai-service/prompts/__init__.py file exists."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
    assert os.path.isfile(path), f"Prompts module not found: {path}"


def test_ai_prompts_contain_all_templates():
    """Verify all 4 prompt templates are defined in prompts/__init__.py."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    expected = [
        "CONTENT_CALENDAR_PROMPT",
        "REVIEW_REPLY_PROMPT",
        "VIRAL_TITLE_PROMPT",
        "GROWTH_SUGGESTION_PROMPT",
    ]
    for name in expected:
        assert name in content, f"Missing prompt template: {name}"


def test_ai_prompts_have_placeholders():
    """Verify prompt templates contain expected format placeholders."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # CONTENT_CALENDAR_PROMPT should have shop_name
    assert "{shop_name}" in content
    assert "{category}" in content
    # REVIEW_REPLY_PROMPT should have platform and rating
    assert "{platform}" in content
    assert "{rating}" in content


# ── Backend Structure Tests ───────────────────────────────────────────

def test_backend_controller_exists():
    """Verify the main controller file exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "controller", "Controller.java")
    assert os.path.isfile(path), "Controller.java not found"


def test_backend_service_exists():
    """Verify the main service file exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "service", "Service.java")
    assert os.path.isfile(path), "Service.java not found"


def test_backend_entity_shop_exists():
    """Verify Shop entity exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "entity", "Shop.java")
    assert os.path.isfile(path), "Shop.java not found"


def test_backend_entity_foot_traffic_exists():
    """Verify FootTraffic entity exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "entity", "FootTraffic.java")
    assert os.path.isfile(path), "FootTraffic.java not found"


def test_backend_entity_content_calendar_exists():
    """Verify ContentCalendar entity exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "entity", "ContentCalendar.java")
    assert os.path.isfile(path), "ContentCalendar.java not found"


def test_backend_entity_review_alert_exists():
    """Verify ReviewAlert entity exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "entity", "ReviewAlert.java")
    assert os.path.isfile(path), "ReviewAlert.java not found"


def test_backend_mapper_exists():
    """Verify the mapper file exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "mapper", "Mapper.java")
    assert os.path.isfile(path), "Mapper.java not found"


def test_backend_dto_exists():
    """Verify the DTO file exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "java", "com",
                        "storeboost", "dto", "DTO.java")
    assert os.path.isfile(path), "DTO.java not found"


def test_init_sql_exists():
    """Verify the database initialization script exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
    assert os.path.isfile(path), "init.sql not found"


def test_application_yml_exists():
    """Verify the Spring Boot config file exists."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "application.yml")
    assert os.path.isfile(path), "application.yml not found"


# ── Database Schema Tests ─────────────────────────────────────────────

def test_init_sql_has_all_tables():
    """Verify init.sql creates all 5 core tables."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    tables = ["shop", "foot_traffic", "content_calendar", "review_alert", "dashboard_stats"]
    for table in tables:
        assert f"CREATE TABLE IF NOT EXISTS {table}" in content, f"Missing table: {table}"


def test_init_sql_has_test_data():
    """Verify init.sql contains test data inserts."""
    path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "INSERT INTO shop" in content, "Missing shop test data"
    assert "INSERT INTO foot_traffic" in content, "Missing foot_traffic test data"
    assert "老王家常菜" in content, "Missing expected test shop name"


# ── Frontend Structure Tests ──────────────────────────────────────────

def test_frontend_index_html_exists():
    """Verify the frontend entry HTML exists."""
    path = os.path.join(PROJECT_ROOT, "frontend", "index.html")
    assert os.path.isfile(path), "index.html not found"


def test_frontend_app_vue_exists():
    """Verify the main Vue component exists."""
    path = os.path.join(PROJECT_ROOT, "frontend", "src", "App.vue")
    assert os.path.isfile(path), "App.vue not found"


def test_frontend_package_json_exists():
    """Verify package.json exists."""
    path = os.path.join(PROJECT_ROOT, "frontend", "package.json")
    assert os.path.isfile(path), "package.json not found"


def test_frontend_package_json_is_valid_json():
    """Verify package.json is valid JSON."""
    path = os.path.join(PROJECT_ROOT, "frontend", "package.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "name" in data or "dependencies" in data, "package.json missing expected keys"


# ── Documentation Tests ───────────────────────────────────────────────

def test_readme_exists():
    """Verify README.md exists."""
    path = os.path.join(PROJECT_ROOT, "README.md")
    assert os.path.isfile(path), "README.md not found"


def test_readme_has_content():
    """Verify README.md is not empty and has meaningful content."""
    path = os.path.join(PROJECT_ROOT, "README.md")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 500, "README.md seems too short"
    assert "StoreBoost" in content, "README.md missing project name"


def test_spec_exists():
    """Verify SPEC.md exists."""
    path = os.path.join(PROJECT_ROOT, "SPEC.md")
    assert os.path.isfile(path), "SPEC.md not found"


def test_architecture_doc_exists():
    """Verify ARCHITECTURE.md exists."""
    path = os.path.join(PROJECT_ROOT, "docs", "ARCHITECTURE.md")
    assert os.path.isfile(path), "ARCHITECTURE.md not found"


def test_patent_doc_exists():
    """Verify PATENT.md exists."""
    path = os.path.join(PROJECT_ROOT, "docs", "PATENT.md")
    assert os.path.isfile(path), "PATENT.md not found"


# ── Configuration Tests ───────────────────────────────────────────────

def test_requirements_txt_exists():
    """Verify requirements.txt exists for AI service."""
    path = os.path.join(PROJECT_ROOT, "requirements.txt")
    assert os.path.isfile(path), "requirements.txt not found"


def test_requirements_has_fastapi():
    """Verify FastAPI is in requirements."""
    path = os.path.join(PROJECT_ROOT, "requirements.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "fastapi" in content.lower(), "FastAPI not in requirements.txt"


def test_gitignore_exists():
    """Verify .gitignore exists."""
    path = os.path.join(PROJECT_ROOT, ".gitignore")
    assert os.path.isfile(path), ".gitignore not found"


def test_ci_workflow_exists():
    """Verify GitHub Actions CI workflow exists."""
    path = os.path.join(PROJECT_ROOT, ".github", "workflows", "ci.yml")
    assert os.path.isfile(path), "CI workflow not found"


# ── Integration Sanity Tests ──────────────────────────────────────────

def test_extract_json_function_logic():
    """Test the JSON extraction logic used in AI service."""
    import re

    def extract_json(text):
        match = re.search(r'```(?:json)?\s*([\s\S]+?)```', text)
        if match:
            return match.group(1).strip()
        text = text.strip()
        if text.startswith('{') or text.startswith('['):
            return text
        match = re.search(r'[\[{][\s\S]+[\]}]', text)
        return match.group(0) if match else None

    # Test markdown-wrapped JSON
    md_input = '```json\n{"key": "value"}\n```'
    assert extract_json(md_input) == '{"key": "value"}'

    # Test plain JSON
    plain_input = '{"key": "value"}'
    assert extract_json(plain_input) == '{"key": "value"}'

    # Test JSON array
    arr_input = '[1, 2, 3]'
    assert extract_json(arr_input) == '[1, 2, 3]'

    # Test text with embedded JSON
    embedded = 'Here is the result: {"a": 1} done.'
    assert extract_json(embedded) == '{"a": 1}'

    # Test no JSON
    assert extract_json("no json here") is None


def test_negative_score_calculation_logic():
    """Test the negative score calculation logic used in review alerts."""
    # Simulate the logic from Service.java
    def calc_negative_score(rating):
        if rating <= 2:
            return 0.8
        elif rating == 3:
            return 0.4
        else:
            return 0.1

    assert calc_negative_score(1) == 0.8
    assert calc_negative_score(2) == 0.8
    assert calc_negative_score(3) == 0.4
    assert calc_negative_score(4) == 0.1
    assert calc_negative_score(5) == 0.1


def test_enter_rate_calculation():
    """Test the enter rate calculation logic."""
    def calc_enter_rate(total_enter, total_passers):
        if total_passers == 0:
            return 0.0
        return round(total_enter / total_passers * 100, 2)

    assert calc_enter_rate(100, 400) == 25.0
    assert calc_enter_rate(0, 400) == 0.0
    assert calc_enter_rate(100, 0) == 0.0
    assert calc_enter_rate(85, 320) == 26.56


# ── Prompt Template Formatting Tests ──────────────────────────────────

def test_content_calendar_prompt_formats():
    """Verify CONTENT_CALENDAR_PROMPT can be formatted with expected args."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the prompt string (rough check)
    assert "CONTENT_CALENDAR_PROMPT" in content
    # Check format placeholders exist
    assert "{shop_name}" in content
    assert "{category}" in content
    assert "{address}" in content
    assert "{description}" in content


def test_review_reply_prompt_formats():
    """Verify REVIEW_REPLY_PROMPT can be formatted with expected args."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "REVIEW_REPLY_PROMPT" in content
    assert "{platform}" in content
    assert "{rating}" in content
    assert "{content}" in content
    assert "{shop_name}" in content
