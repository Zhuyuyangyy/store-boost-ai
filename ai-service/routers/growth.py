"""
StoreBoost AI - Growth Router
===============================
Growth plan generation endpoints.
"""
import logging

from fastapi import APIRouter, Depends

from models import GenerateGrowthPlanRequest, AIResponse
from services import AIService, get_ai_service
from prompts import GROWTH_SUGGESTION_PROMPT

logger = logging.getLogger("storeboost-ai")

router = APIRouter(tags=["growth"])


@router.post("/generate-growth-plan", response_model=AIResponse)
async def generate_growth_plan(
    req: GenerateGrowthPlanRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> AIResponse:
    """Generate AI growth recommendations based on store data."""
    logger.info("Generating growth plan for shop_id=%d", req.shop_id)

    prompt = GROWTH_SUGGESTION_PROMPT.format(
        traffic_data=str(req.traffic_data),
        content_data=str(req.content_data),
        review_data=str(req.review_data),
        shop_info=str(req.shop_info),
    )

    raw = await ai_service.call_llm(prompt, temperature=0.7, max_tokens=2048)
    fallback = {"summary": raw}
    result = ai_service.build_response(raw, fallback_data=fallback)

    return AIResponse(**result)
