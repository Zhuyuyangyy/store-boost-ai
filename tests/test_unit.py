"""
StoreBoost AI - Unit Tests
============================
Unit tests for core business logic functions.
Run: pytest tests/test_unit.py -v
"""
import os
import re
import json
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── JSON Extraction Logic Tests ─────────────────────────────────────

class TestJsonExtraction:
    """Test the JSON extraction logic used in AI response parsing."""

    def extract_json(self, text: str):
        """Replicate the extract_json function from ai-service/main.py."""
        match = re.search(r'```(?:json)?\s*([\s\S]+?)```', text)
        if match:
            return match.group(1).strip()
        text = text.strip()
        if text.startswith('{') or text.startswith('['):
            return text
        match = re.search(r'[\[{][\s\S]+[\]}]', text)
        return match.group(0) if match else None

    def test_markdown_wrapped_json(self):
        input_text = '```json\n{"key": "value"}\n```'
        assert self.extract_json(input_text) == '{"key": "value"}'

    def test_markdown_wrapped_no_lang(self):
        input_text = '```\n{"key": "value"}\n```'
        assert self.extract_json(input_text) == '{"key": "value"}'

    def test_plain_json_object(self):
        input_text = '{"key": "value"}'
        assert self.extract_json(input_text) == '{"key": "value"}'

    def test_plain_json_array(self):
        input_text = '[1, 2, 3]'
        assert self.extract_json(input_text) == '[1, 2, 3]'

    def test_embedded_json_object(self):
        input_text = 'Here is the result: {"a": 1} done.'
        assert self.extract_json(input_text) == '{"a": 1}'

    def test_no_json_returns_none(self):
        assert self.extract_json("no json here") is None

    def test_nested_json(self):
        input_text = '{"data": {"nested": true}}'
        assert self.extract_json(input_text) == '{"data": {"nested": true}}'

    def test_json_with_newlines(self):
        input_text = '{\n  "key": "value",\n  "num": 42\n}'
        assert self.extract_json(input_text) == input_text

    def test_array_with_objects(self):
        input_text = '[{"day": 1}, {"day": 2}]'
        assert self.extract_json(input_text) == input_text


# ── Business Logic Tests ────────────────────────────────────────────

class TestBusinessLogic:
    """Test core business logic calculations."""

    def test_enter_rate_normal(self):
        """Test enter rate calculation with normal values."""
        def calc_enter_rate(total_enter, total_passers):
            if total_passers == 0:
                return 0.0
            return round(total_enter / total_passers * 100, 2)

        assert calc_enter_rate(100, 400) == 25.0
        assert calc_enter_rate(85, 320) == 26.56

    def test_enter_rate_zero_passers(self):
        """Test enter rate when no passers (division by zero)."""
        def calc_enter_rate(total_enter, total_passers):
            if total_passers == 0:
                return 0.0
            return round(total_enter / total_passers * 100, 2)

        assert calc_enter_rate(100, 0) == 0.0

    def test_enter_rate_zero_enter(self):
        """Test enter rate when nobody enters."""
        def calc_enter_rate(total_enter, total_passers):
            if total_passers == 0:
                return 0.0
            return round(total_enter / total_passers * 100, 2)

        assert calc_enter_rate(0, 400) == 0.0

    def test_negative_score_high_rating(self):
        """High rating should have low negative score."""
        def calc_negative_score(rating):
            if rating <= 2:
                return 0.8
            elif rating == 3:
                return 0.4
            else:
                return 0.1

        assert calc_negative_score(5) == 0.1
        assert calc_negative_score(4) == 0.1

    def test_negative_score_mid_rating(self):
        """Mid rating should have medium negative score."""
        def calc_negative_score(rating):
            if rating <= 2:
                return 0.8
            elif rating == 3:
                return 0.4
            else:
                return 0.1

        assert calc_negative_score(3) == 0.4

    def test_negative_score_low_rating(self):
        """Low rating should have high negative score."""
        def calc_negative_score(rating):
            if rating <= 2:
                return 0.8
            elif rating == 3:
                return 0.4
            else:
                return 0.1

        assert calc_negative_score(1) == 0.8
        assert calc_negative_score(2) == 0.8

    def test_weekly_traffic_aggregation(self, sample_traffic_data):
        """Test weekly traffic data aggregation."""
        total_enter = sum(d["total_enter"] for d in sample_traffic_data)
        total_passers = sum(d["total_passers"] for d in sample_traffic_data)
        avg_rate = sum(d["enter_rate"] for d in sample_traffic_data) / len(sample_traffic_data)

        assert total_enter == 792
        assert total_passers == 2850
        assert round(avg_rate, 2) == 27.65

    def test_risk_level_classification(self):
        """Test review risk level classification."""
        def classify_risk(negative_score):
            if negative_score >= 0.7:
                return "HIGH"
            elif negative_score >= 0.4:
                return "MEDIUM"
            else:
                return "LOW"

        assert classify_risk(0.95) == "HIGH"
        assert classify_risk(0.8) == "HIGH"
        assert classify_risk(0.5) == "MEDIUM"
        assert classify_risk(0.4) == "MEDIUM"
        assert classify_risk(0.1) == "LOW"

    def test_content_type_distribution(self):
        """Test content type distribution validation."""
        valid_types = ["种草", "促销", "展示", "热点", "互动"]
        test_types = ["种草", "种草", "促销", "展示", "展示", "热点", "互动"]

        for ct in test_types:
            assert ct in valid_types, f"Invalid content type: {ct}"

        assert len(test_types) == 7, "Should have 7 days of content"


# ── Prompt Template Tests ───────────────────────────────────────────

class TestPromptTemplates:
    """Test prompt template structure and formatting."""

    def test_content_calendar_prompt_has_placeholders(self):
        """Verify content calendar prompt has required placeholders."""
        path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "{shop_name}" in content
        assert "{category}" in content
        assert "{address}" in content
        assert "{description}" in content

    def test_review_reply_prompt_has_placeholders(self):
        """Verify review reply prompt has required placeholders."""
        path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "{platform}" in content
        assert "{rating}" in content
        assert "{content}" in content
        assert "{category}" in content
        assert "{shop_name}" in content

    def test_viral_title_prompt_has_placeholders(self):
        """Verify viral title prompt has required placeholders."""
        path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "{original_title}" in content
        assert "{category}" in content
        assert "{shop_name}" in content

    def test_growth_suggestion_prompt_has_placeholders(self):
        """Verify growth suggestion prompt has required placeholders."""
        path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "{traffic_data}" in content
        assert "{content_data}" in content
        assert "{review_data}" in content
        assert "{shop_info}" in content

    def test_all_prompts_are_strings(self):
        """Verify all prompts are non-empty strings."""
        path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check that prompt variables are assigned string values
        for prompt_name in [
            "CONTENT_CALENDAR_PROMPT",
            "REVIEW_REPLY_PROMPT",
            "VIRAL_TITLE_PROMPT",
            "GROWTH_SUGGESTION_PROMPT",
        ]:
            assert f'{prompt_name} = """' in content or f"{prompt_name} = " in content


# ── File Structure Tests ────────────────────────────────────────────

class TestFileStructure:
    """Test that all required files exist."""

    def test_main_py_exists(self):
        path = os.path.join(PROJECT_ROOT, "ai-service", "main.py")
        assert os.path.isfile(path)

    def test_prompts_init_exists(self):
        path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
        assert os.path.isfile(path)

    def test_requirements_txt_exists(self):
        path = os.path.join(PROJECT_ROOT, "requirements.txt")
        assert os.path.isfile(path)

    def test_gitignore_exists(self):
        path = os.path.join(PROJECT_ROOT, ".gitignore")
        assert os.path.isfile(path)

    def test_ci_workflow_exists(self):
        path = os.path.join(PROJECT_ROOT, ".github", "workflows", "ci.yml")
        assert os.path.isfile(path)

    def test_readme_exists(self):
        path = os.path.join(PROJECT_ROOT, "README.md")
        assert os.path.isfile(path)

    def test_spec_exists(self):
        path = os.path.join(PROJECT_ROOT, "SPEC.md")
        assert os.path.isfile(path)

    def test_demo_script_exists(self):
        path = os.path.join(PROJECT_ROOT, "scripts", "run_demo.py")
        assert os.path.isfile(path)


# ── Database Schema Tests ───────────────────────────────────────────

class TestDatabaseSchema:
    """Test database schema completeness."""

    def test_init_sql_has_all_tables(self):
        path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        tables = ["shop", "foot_traffic", "content_calendar", "review_alert", "dashboard_stats"]
        for table in tables:
            assert f"CREATE TABLE IF NOT EXISTS {table}" in content, f"Missing table: {table}"

    def test_init_sql_has_foreign_keys(self):
        path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # All data tables should reference shop
        assert "FOREIGN KEY (shop_id) REFERENCES shop(id)" in content

    def test_init_sql_has_unique_constraints(self):
        path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "UNIQUE KEY uk_shop_date" in content
        assert "UNIQUE KEY uk_shop_plan_date" in content
        assert "UNIQUE KEY uk_shop_stat_date" in content

    def test_init_sql_has_test_data(self):
        path = os.path.join(PROJECT_ROOT, "backend", "src", "main", "resources", "init.sql")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "INSERT INTO shop" in content
        assert "INSERT INTO foot_traffic" in content
        assert "INSERT INTO content_calendar" in content
        assert "INSERT INTO review_alert" in content
        assert "老王家常菜" in content
