"""
StoreBoost AI - Content Router
================================
Content calendar generation endpoints.
"""
import logging

from fastapi import APIRouter, Depends

from models import GenerateContentRequest, AIResponse
from services import AIService, get_ai_service
from prompts import CONTENT_CALENDAR_PROMPT

logger = logging.getLogger("storeboost-ai")

router = APIRouter(tags=["content"])


@router.post("/generate-content", response_model=AIResponse)
async def generate_content(
    req: GenerateContentRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> AIResponse:
    """Generate a 7-day content calendar for a store."""
    logger.info(
        "Generating content for shop_id=%d, shop_name=%s",
        req.shop_id,
        req.shop_name,
    )

    prompt = CONTENT_CALENDAR_PROMPT.format(
        shop_name=req.shop_name,
        category=req.category,
        address=req.address,
        description=req.description,
    )

    raw = await ai_service.call_llm(prompt, temperature=0.8, max_tokens=4096)
    result = ai_service.build_response(raw)

    return AIResponse(**result)
