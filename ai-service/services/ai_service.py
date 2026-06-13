"""
StoreBoost AI - Core AI Service
=================================
Centralized AI service for NVIDIA NIM API calls.
"""
import logging
from typing import Any
from functools import lru_cache

import httpx
from fastapi import HTTPException

from config import get_settings, get_nvidia_api_key
from utils.json_parser import parse_ai_json

logger = logging.getLogger("storeboost-ai")


class AIService:
    """Service for interacting with NVIDIA NIM API."""

    def __init__(self, api_key: str, base_url: str, model: str, timeout: float):
        """Initialize AI service with configuration.

        Args:
            api_key: NVIDIA API key
            base_url: API base URL
            model: Model identifier
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    async def call_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Call NVIDIA NIM API and return raw content string.

        Args:
            prompt: The prompt to send to the model
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response

        Returns:
            Raw content string from the model

        Raises:
            HTTPException: If API call fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        logger.info(
            "Calling NVIDIA API | model=%s | temp=%.1f | max_tokens=%d",
            self.model,
            temperature,
            max_tokens,
        )

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )

            if resp.status_code != 200:
                logger.error(
                    "NVIDIA API error: %d - %s",
                    resp.status_code,
                    resp.text[:200],
                )
                raise HTTPException(
                    status_code=502,
                    detail=f"NVIDIA API error: {resp.status_code}",
                )

            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            logger.info("NVIDIA API response received | length=%d", len(content))
            return content

        except httpx.TimeoutException:
            logger.error("NVIDIA API timeout after %.1f seconds", self.timeout)
            raise HTTPException(
                status_code=504,
                detail="AI service timeout",
            )
        except httpx.RequestError as e:
            logger.error("NVIDIA API request error: %s", str(e))
            raise HTTPException(
                status_code=502,
                detail=f"AI service connection error: {str(e)}",
            )

    def build_response(self, raw: str, fallback_data: Any = None) -> dict:
        """Build standard API response from AI raw output.

        Args:
            raw: Raw AI response
            fallback_data: Fallback data if parsing fails

        Returns:
            Standard response dict with success/data structure

        Raises:
            HTTPException: If no JSON found and no fallback
        """
        result = parse_ai_json(raw, fallback=fallback_data)
        if result:
            return {"success": True, "data": result}
        if fallback_data is not None:
            return {"success": True, "data": fallback_data}
        raise HTTPException(
            status_code=500,
            detail="AI returned unparseable content",
        )


@lru_cache()
def get_ai_service() -> AIService:
    """Get cached AI service instance."""
    settings = get_settings()
    api_key = get_nvidia_api_key()
    return AIService(
        api_key=api_key,
        base_url=settings.nvidia_base_url,
        model=settings.ai_model,
        timeout=settings.ai_request_timeout,
    )
