"""
StoreBoost AI - Review Router
===============================
Review reply generation endpoints.
"""
import logging

from fastapi import APIRouter, Depends

from models import GenerateReviewReplyRequest, AIResponse
from services import AIService, get_ai_service
from prompts import REVIEW_REPLY_PROMPT

logger = logging.getLogger("storeboost-ai")

router = APIRouter(tags=["review"])


@router.post("/generate-review-reply", response_model=AIResponse)
async def generate_review_reply(
    req: GenerateReviewReplyRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> AIResponse:
    """Generate AI-powered review reply (3 versions + suggestion)."""
    logger.info(
        "Generating review reply for platform=%s, rating=%d",
        req.platform,
        req.rating,
    )

    prompt = REVIEW_REPLY_PROMPT.format(
        platform=req.platform,
        rating=req.rating,
        content=req.content,
        category=req.category,
        shop_name=req.shop_name,
    )

    raw = await ai_service.call_llm(prompt, temperature=0.7, max_tokens=2048)
    fallback = {"reply": raw, "suggestion": ""}
    result = ai_service.build_response(raw, fallback_data=fallback)

    return AIResponse(**result)
