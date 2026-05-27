"""
StoreBoost AI Service - FastAPI AI 层
端口: 8000
被 Spring Boot 后端调用，调用 NVIDIA NIM API
"""

import os
import json
import re
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

# ── 配置 ──────────────────────────────────────────────
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL = "deepseek-ai/deepseek-v4-pro"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY", "storeboost-ai-secret-2026")

# ── 请求模型 ─────────────────────────────────────────
class GenerateContentRequest(BaseModel):
    shop_id: int
    shop_name: str
    category: str
    address: str = ""
    description: str = ""
    days: int = 7

class GenerateReviewReplyRequest(BaseModel):
    platform: str
    rating: int
    content: str
    category: str
    shop_name: str

class GenerateViralTitleRequest(BaseModel):
    original_title: str
    category: str
    shop_name: str

class GenerateGrowthPlanRequest(BaseModel):
    shop_id: int
    traffic_data: dict
    content_data: dict
    review_data: dict
    shop_info: dict

# ── Prompt 模板 ──────────────────────────────────────
from .prompts import (
    CONTENT_CALENDAR_PROMPT,
    REVIEW_REPLY_PROMPT,
    VIRAL_TITLE_PROMPT,
    GROWTH_SUGGESTION_PROMPT
)

# ── FastAPI 应用 ─────────────────────────────────────
app = FastAPI(
    title="StoreBoost AI Service",
    description="AI 内容生成服务",
    version="1.0.0"
)

@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL}

@app.post("/generate-content")
async def generate_content(req: GenerateContentRequest):
    """生成7天内容日历"""
    prompt = CONTENT_CALENDAR_PROMPT.format(
        shop_name=req.shop_name,
        category=req.category,
        address=req.address,
        description=req.description
    )

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 4096
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            json=payload,
            headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"NVIDIA API error: {resp.status_code}")

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    # 提取JSON（可能包裹在markdown代码块中）
    json_str = extract_json(content)
    if not json_str:
        raise HTTPException(status_code=500, detail="AI返回格式错误，无法解析")

    try:
        result = json.loads(json_str)
        return {"success": True, "data": result}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"JSON解析失败: {content[:200]}")

@app.post("/generate-review-reply")
async def generate_review_reply(req: GenerateReviewReplyRequest):
    """生成差评回复"""
    prompt = REVIEW_REPLY_PROMPT.format(
        platform=req.platform,
        rating=req.rating,
        content=req.content,
        category=req.category,
        shop_name=req.shop_name
    )

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            json=payload,
            headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"NVIDIA API error: {resp.status_code}")

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    json_str = extract_json(content)
    if not json_str:
        return {"success": True, "data": {"reply": content, "suggestion": ""}}

    try:
        result = json.loads(json_str)
        return {"success": True, "data": result}
    except json.JSONDecodeError:
        return {"success": True, "data": {"reply": content, "suggestion": ""}}

@app.post("/generate-viral-title")
async def generate_viral_title(req: GenerateViralTitleRequest):
    """生成爆款标题"""
    prompt = VIRAL_TITLE_PROMPT.format(
        original_title=req.original_title,
        category=req.category,
        shop_name=req.shop_name
    )

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 2048
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            json=payload,
            headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"NVIDIA API error: {resp.status_code}")

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    json_str = extract_json(content)
    if not json_str:
        return {"success": True, "titles": [content]}

    try:
        result = json.loads(json_str)
        return {"success": True, "data": result}
    except json.JSONDecodeError:
        return {"success": True, "titles": [content]}

@app.post("/generate-growth-plan")
async def generate_growth_plan(req: GenerateGrowthPlanRequest):
    """生成增长建议"""
    prompt = GROWTH_SUGGESTION_PROMPT.format(
        traffic_data=str(req.traffic_data),
        content_data=str(req.content_data),
        review_data=str(req.review_data),
        shop_info=str(req.shop_info)
    )

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            json=payload,
            headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"NVIDIA API error: {resp.status_code}")

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    json_str = extract_json(content)
    if not json_str:
        return {"success": True, "data": {"summary": content}}

    try:
        result = json.loads(json_str)
        return {"success": True, "data": result}
    except json.JSONDecodeError:
        return {"success": True, "data": {"summary": content}}

def extract_json(text: str) -> Optional[str]:
    """从文本中提取JSON（处理markdown代码块）"""
    # 尝试用markdown代码块包裹的JSON
    match = re.search(r'```(?:json)?\s*([\s\S]+?)```', text)
    if match:
        return match.group(1).strip()

    # 尝试直接解析
    text = text.strip()
    if text.startswith('{') or text.startswith('['):
        return text

    # 查找JSON对象或数组
    match = re.search(r'[\[{][\s\S]+[\]}]', text)
    return match.group(0) if match else None

if __name__ == "__main__":
    import uvicorn
    print(f"StoreBoost AI Service 启动中... 端口: 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")