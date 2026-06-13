# StoreBoost AI - API Documentation

> Version: 1.2.0 | Last updated: 2026-05-29

## Overview

StoreBoost AI exposes two API layers:

1. **Backend API** (Spring Boot, port 8080) - Business logic and data persistence
2. **AI Service API** (FastAPI, port 8000) - AI content generation

---

## AI Service API (FastAPI)

Base URL: `http://localhost:8000`

Interactive documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "model": "deepseek-ai/deepseek-v4-pro",
  "version": "1.2.0"
}
```

---

### Generate Content Calendar

Generate a 7-day content calendar for a store.

```
POST /generate-content
Content-Type: application/json
```

**Request Body:**
```json
{
  "shop_id": 1,
  "shop_name": "老王家常菜",
  "category": "restaurant",
  "address": "北京市朝阳区望京街道",
  "description": "30年老店，家常菜为主",
  "days": 7
}
```

**Field Validation:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `shop_id` | integer | Yes | > 0 |
| `shop_name` | string | Yes | 1-100 chars, no `<>{} ` |
| `category` | string | Yes | 1-50 chars |
| `address` | string | No | max 200 chars |
| `description` | string | No | max 500 chars |
| `days` | integer | No | 1-30, default: 7 |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "day": 1,
      "date": "2026-05-29",
      "content_type": "种草",
      "video_theme": "30年老店的秘密配方",
      "hook_text": "老板透露了一个秘密...",
      "body_text": "...",
      "cta_text": "周末来店里尝尝吧！",
      "hashtags": "#美食 #探店 #望京 #家常菜 #必吃",
      "best_time": "12:00",
      "mood": "温暖"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `422 Unprocessable Entity`: Validation error
- `502 Bad Gateway`: NVIDIA API error
- `500 Internal Server Error`: Processing error

**Example cURL:**
```bash
curl -X POST http://localhost:8000/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": 1,
    "shop_name": "老王家常菜",
    "category": "restaurant",
    "address": "北京市朝阳区望京街道",
    "description": "30年老店，家常菜为主"
  }'
```

---

### Generate Review Reply

Generate AI-powered review replies (3 versions + suggestion).

```
POST /generate-review-reply
Content-Type: application/json
```

**Request Body:**
```json
{
  "platform": "dianping",
  "rating": 2,
  "content": "等了半小时菜才上来，而且菜都凉了",
  "category": "restaurant",
  "shop_name": "老王家常菜"
}
```

**Field Validation:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `platform` | string | Yes | 1-50 chars |
| `rating` | integer | Yes | 1-5 |
| `content` | string | Yes | 5-1000 chars |
| `category` | string | Yes | 1-50 chars |
| `shop_name` | string | Yes | 1-100 chars |

**Response:**
```json
{
  "success": true,
  "data": {
    "version_a": {
      "style": "诚恳道歉型",
      "reply": "非常抱歉给您带来不好的用餐体验...",
      "action": "已加强后厨出餐流程管理"
    },
    "version_b": {
      "style": "幽默化解型",
      "reply": "...",
      "action": "..."
    },
    "version_c": {
      "style": "专业解释型",
      "reply": "...",
      "action": "..."
    },
    "ai_suggestion": "建议优化后厨出餐流程，设置出餐时间提醒..."
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `422 Unprocessable Entity`: Validation error
- `502 Bad Gateway`: NVIDIA API error

**Example cURL:**
```bash
curl -X POST http://localhost:8000/generate-review-reply \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "dianping",
    "rating": 2,
    "content": "等了半小时菜才上来，而且菜都凉了",
    "category": "restaurant",
    "shop_name": "老王家常菜"
  }'
```

---

### Generate Viral Title

Generate viral title suggestions for short videos.

```
POST /generate-viral-title
Content-Type: application/json
```

**Request Body:**
```json
{
  "original_title": "今天做了一道红烧肉",
  "category": "restaurant",
  "shop_name": "老王家常菜"
}
```

**Field Validation:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `original_title` | string | Yes | 1-200 chars |
| `category` | string | Yes | 1-50 chars |
| `shop_name` | string | Yes | 1-100 chars |

**Response:**
```json
{
  "success": true,
  "data": {
    "titles": [
      "30年老店的红烧肉配方终于公开了！🍖",
      "在望京吃了10家红烧肉，这家最绝！",
      "老板说这道菜他自己都吃不腻..."
    ],
    "best_pick": "30年老店的红烧肉配方终于公开了！🍖",
    "reason": "数字+悬念+emoji组合，吸引好奇心"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `422 Unprocessable Entity`: Validation error
- `502 Bad Gateway`: NVIDIA API error

**Example cURL:**
```bash
curl -X POST http://localhost:8000/generate-viral-title \
  -H "Content-Type: application/json" \
  -d '{
    "original_title": "今天做了一道红烧肉",
    "category": "restaurant",
    "shop_name": "老王家常菜"
  }'
```

---

### Generate Growth Plan

Generate AI growth recommendations based on store data.

```
POST /generate-growth-plan
Content-Type: application/json
```

**Request Body:**
```json
{
  "shop_id": 1,
  "traffic_data": {
    "weekly_total": 2850,
    "avg_enter_rate": 27.65,
    "peak_day": "周六"
  },
  "content_data": {
    "published": 5,
    "total_views": 12000,
    "avg_engagement": 3.5
  },
  "review_data": {
    "total": 15,
    "negative": 2,
    "avg_rating": 4.2
  },
  "shop_info": {
    "name": "老王家常菜",
    "category": "restaurant",
    "location": "望京"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": "本周客流稳定，但差评需要重点关注",
    "strengths": ["客流稳定增长", "内容互动率高"],
    "weaknesses": ["差评响应不及时", "高峰时段服务压力大"],
    "top3_actions": [
      {
        "priority": 1,
        "action": "建立差评30分钟响应机制",
        "reason": "本周2条差评未及时回复",
        "expected_impact": "差评转化率降低50%"
      }
    ],
    "content_suggestion": "下周重点发布后厨展示类内容，增强信任感"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `422 Unprocessable Entity`: Validation error
- `502 Bad Gateway`: NVIDIA API error

**Example cURL:**
```bash
curl -X POST http://localhost:8000/generate-growth-plan \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": 1,
    "traffic_data": {"weekly_total": 2850},
    "content_data": {"published": 5},
    "review_data": {"negative": 2},
    "shop_info": {"name": "老王家常菜", "category": "restaurant"}
  }'
```

---

## Error Responses

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "rating"],
      "msg": "ensure this value is less than or equal to 5",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 5}
    }
  ]
}
```

### AI Service Error (502)
```json
{
  "detail": "NVIDIA API error: 429"
}
```

### Internal Error (500)
```json
{
  "detail": "AI returned unparseable content"
}
```

---

## Backend API (Spring Boot)

Base URL: `http://localhost:8080`

### Shop Management

#### Register Shop
```
POST /api/shop/register
Content-Type: application/json

{
  "name": "Store Name",
  "category": "restaurant|beauty|retail|gym|pet",
  "address": "Full address",
  "contact": "Phone number",
  "description": "Store description"
}

Response:
{
  "success": true,
  "shopId": 1,
  "message": "Registration successful"
}
```

#### Get Shop List
```
GET /api/shop/list

Response:
{
  "success": true,
  "data": [...]
}
```

#### Get Shop by ID
```
GET /api/shop/{id}

Response:
{
  "success": true,
  "data": { ... }
}
```

### Foot Traffic

#### Save Traffic Data
```
POST /api/foot-traffic
Content-Type: application/json

{
  "shopId": 1,
  "date": "2026-05-28",
  "totalPassers": 480,
  "totalEnter": 136,
  "avgStaySeconds": 2600,
  "maleRatio": 55.0,
  "femaleRatio": 45.0,
  "peakHour": "12:00,18:30"
}

Response:
{
  "success": true,
  "message": "Saved successfully"
}
```

#### Get Weekly Traffic Trend
```
GET /api/foot-traffic/{shopId}/weekly

Response:
{
  "success": true,
  "data": [
    {
      "date": "2026-05-22",
      "total_passers": 320,
      "total_enter": 85,
      "enter_rate": 26.56
    }
  ]
}
```

### Content Calendar

#### Create Content Entry
```
POST /api/content/calendar
Content-Type: application/json

{
  "shopId": 1,
  "planDate": "2026-05-29",
  "contentType": "seeding|promotion|showcase|hotspot|interaction",
  "videoTheme": "Video theme description"
}

Response:
{
  "success": true,
  "id": 1,
  "message": "Calendar entry created"
}
```

#### Get Calendar by Shop
```
GET /api/content/calendar/{shopId}

Response:
{
  "success": true,
  "data": [...]
}
```

#### Generate AI Script
```
POST /api/content/script/generate
Content-Type: application/json

{
  "calendarId": 1,
  "shopName": "Store Name",
  "category": "restaurant",
  "city": "Beijing"
}

Response:
{
  "success": true,
  "hook": "Opening hook text",
  "body": "Full script body",
  "cta": "Call to action",
  "hashtags": "#tag1 #tag2",
  "bestTime": "12:00,19:00"
}
```

### Review Management

#### Sync Review
```
POST /api/review/sync
Content-Type: application/json

{
  "shopId": 1,
  "platform": "dianping|meituan|xiaohongshu|douyin",
  "reviewerName": "Username",
  "rating": 2,
  "content": "Review text"
}

Response:
{
  "success": true,
  "message": "Review synced"
}
```

#### Get Alerts
```
GET /api/review/alerts/{shopId}

Response:
{
  "success": true,
  "data": [...]
}
```

#### Save Reply
```
POST /api/review/reply
Content-Type: application/json

{
  "alertId": 1,
  "reply": "Reply text"
}

Response:
{
  "success": true,
  "message": "Reply saved"
}
```

### Dashboard

#### Get Dashboard Data
```
GET /api/dashboard/{shopId}

Response:
{
  "success": true,
  "shop": { ... },
  "traffic": [...],
  "calendars": [...],
  "alertCount": 5,
  "pendingAlerts": 2,
  "message": "Data loaded"
}
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NVIDIA_API_KEY` | NVIDIA API key | (required) |
| `NVIDIA_BASE_URL` | API base URL | `https://integrate.api.nvidia.com/v1` |
| `AI_MODEL` | Model identifier | `deepseek-ai/deepseek-v4-pro` |
| `AI_REQUEST_TIMEOUT` | Request timeout (seconds) | `120.0` |
| `APP_HOST` | Server host | `0.0.0.0` |
| `APP_PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000,http://localhost:5173` |

---

## Rate Limiting

| Tier | Limit |
|------|-------|
| Free | 20 requests/hour per store |
| Paid | 100 requests/hour per store |

---

## SDK Examples

### Python
```python
import httpx

async def generate_content(shop_name: str, category: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/generate-content",
            json={
                "shop_id": 1,
                "shop_name": shop_name,
                "category": category,
            }
        )
        return response.json()
```

### JavaScript
```javascript
async function generateContent(shopName, category) {
  const response = await fetch('http://localhost:8000/generate-content', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      shop_id: 1,
      shop_name: shopName,
      category: category,
    })
  });
  return response.json();
}
```

---

*Last updated: 2026-05-29*
