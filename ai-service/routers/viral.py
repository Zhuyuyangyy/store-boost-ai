"""
StoreBoost AI - Viral Title Router
=====================================
Viral title generation endpoints.
"""
import logging

from fastapi import APIRouter, Depends

from models import GenerateViralTitleRequest, AIResponse
from services import AIService, get_ai_service
from prompts import VIRAL_TITLE_PROMPT

logger = logging.getLogger("storeboost-ai")

router = APIRouter(tags=["viral"])


@router.post("/generate-viral-title", response_model=AIResponse)
async def generate_viral_title(
    req: GenerateViralTitleRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> AIResponse:
    """Generate viral title suggestions for short videos."""
    logger.info(
        "Generating viral title for category=%s, shop_name=%s",
        req.category,
        req.shop_name,
    )

    prompt = VIRAL_TITLE_PROMPT.format(
        original_title=req.original_title,
        category=req.category,
        shop_name=req.shop_name,
    )

    raw = await ai_service.call_llm(prompt, temperature=0.9, max_tokens=2048)
    fallback = {"titles": [raw]}
    result = ai_service.build_response(raw, fallback_data=fallback)

    return AIResponse(**result)
