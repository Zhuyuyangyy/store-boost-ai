"""
StoreBoost AI - JSON Parser Tests
===================================
Tests for JSON parsing utilities.
"""
import os
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def setup_path():
    """Add ai-service to path."""
    import sys
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "ai-service"))
    yield
    sys.path.pop(0)


class TestExtractJson:
    """Test extract_json function."""

    def test_markdown_wrapped_json(self):
        """Test extraction from markdown-wrapped JSON."""
        from utils.json_parser import extract_json

        input_text = '```json\n{"key": "value"}\n```'
        assert extract_json(input_text) == '{"key": "value"}'

    def test_markdown_wrapped_no_lang(self):
        """Test extraction from markdown without language specifier."""
        from utils.json_parser import extract_json

        input_text = '```\n{"key": "value"}\n```'
        assert extract_json(input_text) == '{"key": "value"}'

    def test_plain_json_object(self):
        """Test extraction from plain JSON object."""
        from utils.json_parser import extract_json

        input_text = '{"key": "value"}'
        assert extract_json(input_text) == '{"key": "value"}'

    def test_plain_json_array(self):
        """Test extraction from plain JSON array."""
        from utils.json_parser import extract_json

        input_text = '[1, 2, 3]'
        assert extract_json(input_text) == '[1, 2, 3]'

    def test_embedded_json_object(self):
        """Test extraction from text with embedded JSON."""
        from utils.json_parser import extract_json

        input_text = 'Here is the result: {"a": 1} done.'
        assert extract_json(input_text) == '{"a": 1}'

    def test_no_json_returns_none(self):
        """Test that no JSON returns None."""
        from utils.json_parser import extract_json

        assert extract_json("no json here") is None

    def test_empty_string_returns_none(self):
        """Test that empty string returns None."""
        from utils.json_parser import extract_json

        assert extract_json("") is None

    def test_none_returns_none(self):
        """Test that None returns None."""
        from utils.json_parser import extract_json

        assert extract_json(None) is None

    def test_nested_json(self):
        """Test extraction of nested JSON."""
        from utils.json_parser import extract_json

        input_text = '{"data": {"nested": true}}'
        assert extract_json(input_text) == '{"data": {"nested": true}}'

    def test_json_with_newlines(self):
        """Test extraction of JSON with newlines."""
        from utils.json_parser import extract_json

        input_text = '{\n  "key": "value",\n  "num": 42\n}'
        assert extract_json(input_text) == input_text

    def test_array_with_objects(self):
        """Test extraction of array with objects."""
        from utils.json_parser import extract_json

        input_text = '[{"day": 1}, {"day": 2}]'
        assert extract_json(input_text) == input_text


class TestParseAiJson:
    """Test parse_ai_json function."""

    def test_valid_json(self):
        """Test parsing valid JSON."""
        from utils.json_parser import parse_ai_json

        raw = '{"key": "value"}'
        result = parse_ai_json(raw)
        assert result == {"key": "value"}

    def test_markdown_json(self):
        """Test parsing markdown-wrapped JSON."""
        from utils.json_parser import parse_ai_json

        raw = '```json\n{"key": "value"}\n```'
        result = parse_ai_json(raw)
        assert result == {"key": "value"}

    def test_fallback_on_invalid_json(self):
        """Test fallback when JSON is invalid."""
        from utils.json_parser import parse_ai_json

        raw = "Not JSON at all"
        fallback = {"default": True}
        result = parse_ai_json(raw, fallback=fallback)
        assert result == fallback

    def test_empty_fallback(self):
        """Test default fallback (empty dict)."""
        from utils.json_parser import parse_ai_json

        raw = "Not JSON"
        result = parse_ai_json(raw)
        assert result == {}

    def test_none_input(self):
        """Test None input."""
        from utils.json_parser import parse_ai_json

        result = parse_ai_json(None)
        assert result == {}


class TestValidateJsonStructure:
    """Test validate_json_structure function."""

    def test_valid_structure(self):
        """Test validation with all required keys."""
        from utils.json_parser import validate_json_structure

        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        required = ["key1", "key2"]
        assert validate_json_structure(data, required) is True

    def test_missing_key(self):
        """Test validation with missing key."""
        from utils.json_parser import validate_json_structure

        data = {"key1": "value1"}
        required = ["key1", "key2"]
        assert validate_json_structure(data, required) is False

    def test_empty_required(self):
        """Test validation with empty required keys."""
        from utils.json_parser import validate_json_structure

        data = {"key1": "value1"}
        assert validate_json_structure(data, []) is True

    def test_empty_data(self):
        """Test validation with empty data."""
        from utils.json_parser import validate_json_structure

        required = ["key1"]
        assert validate_json_structure({}, required) is False
