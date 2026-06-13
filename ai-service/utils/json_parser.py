"""
StoreBoost AI - JSON Parsing Utilities
========================================
Extract and parse JSON from AI responses.
"""
import json
import re
from typing import Any, Optional


def extract_json(text: str) -> Optional[str]:
    """Extract JSON string from text (handles markdown code blocks).

    Args:
        text: Raw text potentially containing JSON

    Returns:
        Extracted JSON string or None if no JSON found
    """
    if not text or not text.strip():
        return None

    # Try markdown-wrapped JSON
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if match:
        return match.group(1).strip()

    # Try direct parse
    text = text.strip()
    if text.startswith("{") or text.startswith("["):
        return text

    # Find embedded JSON object or array
    match = re.search(r"[\[{][\s\S]+[\]}]", text)
    return match.group(0) if match else None


def parse_ai_json(raw: str, fallback: Any = None) -> dict:
    """Extract and parse JSON from AI response (handles markdown wrapping).

    Args:
        raw: Raw AI response text
        fallback: Default value if parsing fails

    Returns:
        Parsed dict on success, or fallback if parsing fails
    """
    json_str = extract_json(raw)
    if not json_str:
        return fallback if fallback is not None else {}

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return fallback if fallback is not None else {}


def validate_json_structure(data: dict, required_keys: list[str]) -> bool:
    """Validate that a dict contains all required keys.

    Args:
        data: Dictionary to validate
        required_keys: List of required keys

    Returns:
        True if all keys present, False otherwise
    """
    return all(key in data for key in required_keys)
