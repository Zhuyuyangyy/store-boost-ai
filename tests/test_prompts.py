"""
StoreBoost AI - Prompt Template Tests
======================================
Comprehensive tests for prompt templates and their formatting.
Run: pytest tests/test_prompts.py -v
"""
import os
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def prompts_content():
    """Load the prompts module content."""
    path = os.path.join(PROJECT_ROOT, "ai-service", "prompts", "__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def prompt_templates():
    """Import prompt templates as Python objects."""
    from prompts import (
        CONTENT_CALENDAR_PROMPT,
        REVIEW_REPLY_PROMPT,
        VIRAL_TITLE_PROMPT,
        GROWTH_SUGGESTION_PROMPT,
    )
    return {
        "content_calendar": CONTENT_CALENDAR_PROMPT,
        "review_reply": REVIEW_REPLY_PROMPT,
        "viral_title": VIRAL_TITLE_PROMPT,
        "growth_suggestion": GROWTH_SUGGESTION_PROMPT,
    }


# ── Template Existence Tests ────────────────────────────────────────

class TestPromptExistence:
    """Verify all prompt templates exist and are non-empty."""

    def test_all_prompts_defined(self, prompt_templates):
        """All 4 prompt templates should be defined."""
        assert len(prompt_templates) == 4
        for name, template in prompt_templates.items():
            assert template is not None, f"{name} is None"
            assert len(template) > 100, f"{name} is too short ({len(template)} chars)"

    def test_content_calendar_not_empty(self, prompt_templates):
        """Content calendar prompt should be substantial."""
        assert len(prompt_templates["content_calendar"]) > 500

    def test_review_reply_not_empty(self, prompt_templates):
        """Review reply prompt should be substantial."""
        assert len(prompt_templates["review_reply"]) > 500

    def test_viral_title_not_empty(self, prompt_templates):
        """Viral title prompt should be substantial."""
        assert len(prompt_templates["viral_title"]) > 300

    def test_growth_suggestion_not_empty(self, prompt_templates):
        """Growth suggestion prompt should be substantial."""
        assert len(prompt_templates["growth_suggestion"]) > 300


# ── Placeholder Tests ───────────────────────────────────────────────

class TestPlaceholders:
    """Verify all required placeholders exist in each template."""

    def test_content_calendar_placeholders(self, prompt_templates):
        """Content calendar should have shop info placeholders."""
        tpl = prompt_templates["content_calendar"]
        required = ["{shop_name}", "{category}", "{address}", "{description}"]
        for ph in required:
            assert ph in tpl, f"Missing placeholder: {ph}"

    def test_review_reply_placeholders(self, prompt_templates):
        """Review reply should have review info placeholders."""
        tpl = prompt_templates["review_reply"]
        required = ["{platform}", "{rating}", "{content}", "{category}", "{shop_name}"]
        for ph in required:
            assert ph in tpl, f"Missing placeholder: {ph}"

    def test_viral_title_placeholders(self, prompt_templates):
        """Viral title should have title info placeholders."""
        tpl = prompt_templates["viral_title"]
        required = ["{original_title}", "{category}", "{shop_name}"]
        for ph in required:
            assert ph in tpl, f"Missing placeholder: {ph}"

    def test_growth_suggestion_placeholders(self, prompt_templates):
        """Growth suggestion should have data placeholders."""
        tpl = prompt_templates["growth_suggestion"]
        required = ["{traffic_data}", "{content_data}", "{review_data}", "{shop_info}"]
        for ph in required:
            assert ph in tpl, f"Missing placeholder: {ph}"


# ── Template Formatting Tests ───────────────────────────────────────

class TestTemplateFormatting:
    """Verify templates can be formatted without errors."""

    def test_content_calendar_formats(self, prompt_templates):
        """Content calendar should format with valid args."""
        result = prompt_templates["content_calendar"].format(
            shop_name="Test Shop",
            category="restaurant",
            address="123 Street",
            description="A test shop",
        )
        assert "Test Shop" in result
        assert "restaurant" in result

    def test_review_reply_formats(self, prompt_templates):
        """Review reply should format with valid args."""
        result = prompt_templates["review_reply"].format(
            platform="dianping",
            rating=2,
            content="Bad food",
            category="restaurant",
            shop_name="Test Shop",
        )
        assert "dianping" in result
        assert "Bad food" in result

    def test_viral_title_formats(self, prompt_templates):
        """Viral title should format with valid args."""
        result = prompt_templates["viral_title"].format(
            original_title="Test Title",
            category="restaurant",
            shop_name="Test Shop",
        )
        assert "Test Title" in result

    def test_growth_suggestion_formats(self, prompt_templates):
        """Growth suggestion should format with valid args."""
        result = prompt_templates["growth_suggestion"].format(
            traffic_data="{}",
            content_data="{}",
            review_data="{}",
            shop_info="{}",
        )
        assert len(result) > 100


# ── Content Quality Tests ───────────────────────────────────────────

class TestPromptContentQuality:
    """Verify prompt templates contain quality guidance."""

    def test_content_calendar_has_strategy(self, prompt_templates):
        """Content calendar should include content strategy."""
        tpl = prompt_templates["content_calendar"]
        assert "种草" in tpl or "seeding" in tpl.lower()
        assert "促销" in tpl or "promotion" in tpl.lower()
        assert "钩子" in tpl or "hook" in tpl.lower()

    def test_content_calendar_has_json_format(self, prompt_templates):
        """Content calendar should specify JSON output format."""
        tpl = prompt_templates["content_calendar"]
        assert "json" in tpl.lower() or "JSON" in tpl

    def test_review_reply_has_risk_levels(self, prompt_templates):
        """Review reply should define risk levels."""
        tpl = prompt_templates["review_reply"]
        assert "1星" in tpl or "1 star" in tpl.lower()
        assert "道歉" in tpl or "apolog" in tpl.lower()

    def test_viral_title_has_formulas(self, prompt_templates):
        """Viral title should include title formulas."""
        tpl = prompt_templates["viral_title"]
        assert "数字" in tpl or "悬念" in tpl or "情绪" in tpl

    def test_growth_suggestion_has_analysis_dimensions(self, prompt_templates):
        """Growth suggestion should define analysis dimensions."""
        tpl = prompt_templates["growth_suggestion"]
        assert "客流" in tpl or "traffic" in tpl.lower()
        assert "内容" in tpl or "content" in tpl.lower()
        assert "差评" in tpl or "review" in tpl.lower()


# ── Helper Function Tests ───────────────────────────────────────────

class TestPromptHelperFunctions:
    """Test the helper functions in prompts module."""

    def test_build_content_calendar_prompt(self):
        """Test build_content_calendar_prompt helper."""
        from prompts import build_content_calendar_prompt

        result = build_content_calendar_prompt({
            "name": "Test Shop",
            "category": "restaurant",
            "address": "123 Street",
            "description": "A test shop",
        })
        assert "Test Shop" in result
        assert "restaurant" in result

    def test_build_viral_title_prompt(self):
        """Test build_viral_title_prompt helper."""
        from prompts import build_viral_title_prompt

        result = build_viral_title_prompt("Test Title", "restaurant", "Test Shop")
        assert "Test Title" in result
        assert "Test Shop" in result

    def test_build_review_reply_prompt(self):
        """Test build_review_reply_prompt helper."""
        from prompts import build_review_reply_prompt

        result = build_review_reply_prompt(
            platform="dianping",
            rating=2,
            content="Bad food",
            category="restaurant",
            shop_name="Test Shop",
        )
        assert "dianping" in result
        assert "Bad food" in result

    def test_build_review_reply_with_negative_type(self):
        """Test build_review_reply_prompt with custom negative type."""
        from prompts import build_review_reply_prompt

        result = build_review_reply_prompt(
            platform="dianping",
            rating=1,
            content="Terrible",
            category="restaurant",
            shop_name="Test Shop",
            negative_type="服务态度问题",
        )
        assert "服务态度问题" in result

    def test_build_growth_suggestion_prompt(self):
        """Test build_growth_suggestion_prompt helper."""
        from prompts import build_growth_suggestion_prompt

        result = build_growth_suggestion_prompt(
            traffic_data={"avg_rate": 25.0},
            content_data={"published": 5},
            review_data={"negative": 2},
            shop_info={"name": "Test"},
        )
        assert len(result) > 100
