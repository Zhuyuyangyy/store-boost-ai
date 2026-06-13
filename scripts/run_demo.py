#!/usr/bin/env python3
"""
StoreBoost AI - Demo Script
============================
Demonstrates the AI content generation capabilities without requiring
a running backend or NVIDIA API key.

Usage:
    python scripts/run_demo.py              # Run full demo
    python scripts/run_demo.py --mock       # Run with mock AI (no API key needed)
    python scripts/run_demo.py --live       # Run against live AI service (needs API key)

Prerequisites:
    pip install httpx python-dotenv
"""
import asyncio
import json
import os
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Demo Store Data ───────────────────────────────────────────────────

DEMO_STORES = [
    {
        "name": "老王家常菜",
        "category": "餐饮",
        "address": "北京市朝阳区望京街道",
        "description": "20年地道家常菜，招牌红烧肉，人气爆满",
    },
    {
        "name": "美颜阁美容店",
        "category": "美业",
        "address": "上海市静安区南京西路",
        "description": "专业美容护理，皮肤管理，会员制服务",
    },
    {
        "name": "动杰健身房",
        "category": "健身房",
        "address": "广州市天河区天河路",
        "description": "24小时营业，器械齐全，私教一对一",
    },
]

DEMO_REVIEWS = [
    {
        "platform": "dianping",
        "rating": 2,
        "content": "等位等了40分钟，菜上来都凉了，服务态度也不好",
        "category": "餐饮",
        "shop_name": "老王家常菜",
    },
    {
        "platform": "meituan",
        "rating": 1,
        "content": "点的红烧肉明显是预制菜，跟图片差太多，坑人！",
        "category": "餐饮",
        "shop_name": "老王家常菜",
    },
    {
        "platform": "xiaohongshu",
        "rating": 3,
        "content": "环境一般般，价格倒是不贵，味道还行吧",
        "category": "餐饮",
        "shop_name": "老王家常菜",
    },
]

DEMO_TRAFFIC = [
    {"date": "2026-05-22", "total_passers": 320, "total_enter": 85, "enter_rate": 26.56},
    {"date": "2026-05-23", "total_passers": 380, "total_enter": 102, "enter_rate": 26.84},
    {"date": "2026-05-24", "total_passers": 290, "total_enter": 78, "enter_rate": 26.90},
    {"date": "2026-05-25", "total_passers": 410, "total_enter": 115, "enter_rate": 28.05},
    {"date": "2026-05-26", "total_passers": 450, "total_enter": 128, "enter_rate": 28.44},
    {"date": "2026-05-27", "total_passers": 520, "total_enter": 148, "enter_rate": 28.46},
    {"date": "2026-05-28", "total_passers": 480, "total_enter": 136, "enter_rate": 28.33},
]


# ── Mock AI Responses ─────────────────────────────────────────────────

MOCK_CONTENT_CALENDAR = [
    {
        "day": 1,
        "date": "2026-05-29",
        "content_type": "种草",
        "video_theme": "招牌红烧肉的秘密",
        "hook_text": "老板们！这道红烧肉我能吃三碗饭！",
        "body_text": "今天揭秘我们后厨的秘密。每天早上6点，我们就去采购最新鲜的五花肉，炖足3个小时，看这色泽，闻这香味，保证你吃一口就停不下来。",
        "cta_text": "看完记得点赞关注，老王在这里等你们！",
        "hashtags": "#老王家常菜 #红烧肉 #家常菜 #美食 #北京探店",
        "best_time": "12:00",
        "mood": "温暖",
    },
    {
        "day": 2,
        "date": "2026-05-30",
        "content_type": "促销",
        "video_theme": "周年庆优惠大放送",
        "hook_text": "周年庆来了，全场8折！错过再等一年！",
        "body_text": "感谢新老客户20年的支持，周年庆期间全场8折，充值500送100，还有神秘菜品免费送！",
        "cta_text": "快来门店吧，晚了就没位置了！",
        "hashtags": "#老王家常菜 #周年庆 #优惠 #北京美食 #限时活动",
        "best_time": "19:00",
        "mood": "活力",
    },
    {
        "day": 3,
        "date": "2026-05-31",
        "content_type": "展示",
        "video_theme": "后厨大揭秘",
        "hook_text": "带你看看真正的后厨！99%的人都没见过！",
        "body_text": "每天新鲜食材，现做现卖，干净卫生，每一道菜都是用心做的。来看看我们的厨房标准吧。",
        "cta_text": "关注我，更多探店内容等你来看！",
        "hashtags": "#老王家常菜 #后厨 #探店 #食品安全 #放心吃",
        "best_time": "18:00",
        "mood": "专业",
    },
    {
        "day": 4,
        "date": "2026-06-01",
        "content_type": "热点",
        "video_theme": "六一儿童节亲子套餐",
        "hook_text": "六一来了！带孩子来这里，全家都开心！",
        "body_text": "六一儿童节特别推出亲子套餐，大人小孩都能吃好，还有小礼物送哦！",
        "cta_text": "赶紧预约，位置有限！",
        "hashtags": "#老王家常菜 #六一 #亲子 #家庭聚餐 #北京美食",
        "best_time": "11:00",
        "mood": "温暖",
    },
    {
        "day": 5,
        "date": "2026-06-02",
        "content_type": "展示",
        "video_theme": "员工风采展示",
        "hook_text": "认识一下我们的大厨！20年功力！",
        "body_text": "我们的厨师团队平均从业15年以上，每一道菜都凝聚着匠心。今天带你认识一下我们的主厨老张。",
        "cta_text": "点赞支持我们的厨师团队！",
        "hashtags": "#老王家常菜 #厨师 #匠心 #团队 #美食背后",
        "best_time": "14:00",
        "mood": "温暖",
    },
    {
        "day": 6,
        "date": "2026-06-03",
        "content_type": "种草",
        "video_theme": "必点TOP3菜品",
        "hook_text": "来老王家必点这3道菜！本地人都知道！",
        "body_text": "第一名红烧肉，第二名糖醋里脊，第三名地三鲜。这三道菜是我们店的招牌，每一道都值得你专程来吃。",
        "cta_text": "你最想吃哪道？评论区告诉我！",
        "hashtags": "#老王家常菜 #必吃 #TOP3 #家常菜 #北京探店",
        "best_time": "12:00",
        "mood": "活力",
    },
    {
        "day": 7,
        "date": "2026-06-04",
        "content_type": "互动",
        "video_theme": "猜价格挑战",
        "hook_text": "这桌菜猜猜多少钱？猜对有奖！",
        "body_text": "今天点了4菜1汤，看看这分量和品质，猜猜总共多少钱？评论区猜对的朋友，下次来店送一份招牌凉菜！",
        "cta_text": "快来评论区猜价格吧！",
        "hashtags": "#老王家常菜 #猜价格 #互动 #美食挑战 #北京美食",
        "best_time": "19:00",
        "mood": "幽默",
    },
]

MOCK_REVIEW_REPLIES = {
    "version_a": {
        "style": "诚恳道歉型",
        "reply": "非常抱歉给您带来不好的体验，等位时间长确实是我们的问题。我们已优化了排队管理系统，并增加了等位区的舒适度。送您一张8折优惠券，期待您的再次光临！",
        "action": "已安装叫号系统，增加等位座椅，高峰期增派服务员",
    },
    "version_b": {
        "style": "幽默化解型",
        "reply": "看来我们的红烧肉太受欢迎了，让您等了这么久！不过放心，下次来直接报暗号'老王最帅'，优先安排座位！哈哈，期待再次为您服务~",
        "action": "优化出餐流程，高峰期提前备菜",
    },
    "version_c": {
        "style": "专业解释型",
        "reply": "感谢您的反馈。关于等位问题，我们已增设预约通道；关于菜品温度，我们已升级保温设备。您的意见是我们改进的动力，欢迎再次体验。",
        "action": "新增预约系统，升级保温设备，加强服务培训",
    },
    "ai_suggestion": "建议：1. 优化高峰期排队管理，引入预约制；2. 加强出餐速度，高峰期提前备菜；3. 等位区增加小食和饮品，提升等待体验；4. 建立服务响应机制，减少顾客不满。",
}

MOCK_GROWTH_PLAN = {
    "summary": "本周进店率稳步提升，但差评处理仍需加强，建议重点优化服务响应速度。",
    "strengths": ["进店率连续7天增长，趋势良好", "内容发布频率稳定，覆盖多种类型", "高峰时段客流集中，转化潜力大"],
    "weaknesses": ["差评响应速度慢，影响口碑", "互动型内容偏少，用户粘性不足"],
    "top3_actions": [
        {
            "priority": 1,
            "action": "建立差评2小时响应机制，AI辅助生成回复",
            "reason": "差评响应时间直接影响店铺评分和搜索排名",
            "expected_impact": "差评处理效率提升80%，评分预计回升0.3分",
        },
        {
            "priority": 2,
            "action": "增加互动型内容比例，每周至少2条",
            "reason": "互动型内容能提升用户参与度和分享率",
            "expected_impact": "互动率提升50%，新增粉丝预计+200/周",
        },
        {
            "priority": 3,
            "action": "优化发布时间，种草内容集中在11:30-12:30",
            "reason": "数据显示午间是内容曝光的黄金时段",
            "expected_impact": "内容曝光量预计提升30%",
        },
    ],
    "content_suggestion": "下周内容方向：聚焦'夏日限定'主题，推出清凉菜品展示，结合高温天气做'解暑美食'系列内容。",
    "warning_signs": ["竞品'张家小馆'近期内容频率增加，需关注", "差评中反复出现'等位时间长'，需根本性解决"],
}


# ── Display Helpers ───────────────────────────────────────────────────

def print_header(title: str):
    """Print a styled section header."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_json(data, indent=2):
    """Print JSON data with syntax highlighting."""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def print_metric(label: str, value, trend: str = ""):
    """Print a metric card."""
    trend_str = f"  {trend}" if trend else ""
    print(f"  {label}: {value}{trend_str}")


# ── Demo Functions ────────────────────────────────────────────────────

def demo_traffic_dashboard():
    """Display the traffic dashboard demo."""
    print_header("1. Traffic Dashboard - Traffic Trends (Past 7 Days)")

    total_enter = sum(d["total_enter"] for d in DEMO_TRAFFIC)
    avg_rate = sum(d["enter_rate"] for d in DEMO_TRAFFIC) / len(DEMO_TRAFFIC)

    print_metric("Weekly Total Visitors", total_enter)
    print_metric("Average Entry Rate", f"{avg_rate:.2f}%")
    print_metric("Peak Day", "2026-05-27 (148 visitors)")

    print("\n  Daily Breakdown:")
    print(f"  {'Date':<14} {'Passers':>8} {'Entered':>8} {'Rate':>8}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8}")
    for d in DEMO_TRAFFIC:
        bar_len = int(d["enter_rate"] / 5)
        bar = "#" * bar_len
        print(f"  {d['date']:<14} {d['total_passers']:>8} {d['total_enter']:>8} {d['enter_rate']:>7.2f}%  {bar}")


def demo_content_calendar():
    """Display the AI-generated content calendar demo."""
    print_header("2. AI Content Calendar - 7-Day Video Plan")

    store = DEMO_STORES[0]
    print(f"\n  Store: {store['name']} ({store['category']})")
    print(f"  Address: {store['address']}")
    print(f"  Generated: 7 content plans\n")

    for item in MOCK_CONTENT_CALENDAR:
        status = "Published" if item["day"] == 1 else "Pending"
        print(f"  Day {item['day']} [{item['content_type']}] - {item['video_theme']}")
        print(f"    Hook: {item['hook_text']}")
        print(f"    Best Time: {item['best_time']} | Mood: {item['mood']} | Status: {status}")
        print(f"    Tags: {item['hashtags']}")
        print()


def demo_review_reply():
    """Display the AI review reply demo."""
    print_header("3. AI Review Reply - Negative Review Management")

    review = DEMO_REVIEWS[0]
    print(f"\n  Platform: {review['platform']}")
    print(f"  Rating: {review['rating']} stars")
    print(f"  Content: {review['content']}")
    print(f"  Risk Level: HIGH (score: 0.80)")
    print(f"\n  AI Generated Replies (3 versions):\n")

    for key, reply in MOCK_REVIEW_REPLIES.items():
        if key.startswith("version"):
            print(f"  [{reply['style']}]")
            print(f"    Reply: {reply['reply']}")
            print(f"    Action: {reply['action']}")
            print()

    print(f"  [AI Suggestion]")
    print(f"    {MOCK_REVIEW_REPLIES['ai_suggestion']}")


def demo_growth_plan():
    """Display the AI growth plan demo."""
    print_header("4. AI Growth Plan - Weekly Analysis Report")

    plan = MOCK_GROWTH_PLAN
    print(f"\n  Summary: {plan['summary']}")

    print(f"\n  Strengths:")
    for s in plan["strengths"]:
        print(f"    + {s}")

    print(f"\n  Weaknesses:")
    for w in plan["weaknesses"]:
        print(f"    - {w}")

    print(f"\n  Top 3 Actions:")
    for a in plan["top3_actions"]:
        print(f"    #{a['priority']} {a['action']}")
        print(f"       Reason: {a['reason']}")
        print(f"       Expected Impact: {a['expected_impact']}")
        print()

    print(f"  Content Suggestion: {plan['content_suggestion']}")

    print(f"\n  Warning Signs:")
    for w in plan["warning_signs"]:
        print(f"    ! {w}")


def demo_business_metrics():
    """Display business value metrics."""
    print_header("5. Business Value Metrics")

    print("\n  Per-Store Monthly Value:")
    print(f"  {'Item':<30} {'Traditional':>12} {'StoreBoost':>12} {'Savings':>12}")
    print(f"  {'-'*30} {'-'*12} {'-'*12} {'-'*12}")
    metrics = [
        ("Content Production", "3000 RMB", "0 RMB", "+3000"),
        ("Review Management", "2500 RMB", "500 RMB", "+2000"),
        ("Ad Optimization", "5000 RMB", "4000 RMB", "+1000"),
        ("Traffic Growth Revenue", "-", "+3000 RMB", "+3000"),
        ("Customer Value Uplift", "-", "+1600 RMB", "+1600"),
    ]
    for item, trad, boost, saving in metrics:
        print(f"  {item:<30} {trad:>12} {boost:>12} {saving:>12}")

    print(f"\n  Monthly Net Benefit: +10,600 RMB/store")
    print(f"  Annual Net Benefit: +127,200 RMB/store")
    print(f"  ROI: 1060%")


async def demo_live_ai_service():
    """Run demo against the live AI service (requires API key)."""
    import httpx

    print_header("Live AI Service Demo")

    ai_url = os.getenv("AI_SERVICE_URL", "http://localhost:8000")

    # Health check
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{ai_url}/health")
            if resp.status_code == 200:
                print(f"\n  AI Service: ONLINE at {ai_url}")
                print(f"  Model: {resp.json().get('model', 'unknown')}")
            else:
                print(f"\n  AI Service: ERROR (status {resp.status_code})")
                return
    except Exception as e:
        print(f"\n  AI Service: OFFLINE ({e})")
        print("  Start with: cd ai-service && python main.py")
        return

    # Generate content
    store = DEMO_STORES[0]
    print(f"\n  Generating content for: {store['name']}...")
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{ai_url}/generate-content",
                json={
                    "shop_id": 1,
                    "shop_name": store["name"],
                    "category": store["category"],
                    "address": store["address"],
                    "description": store["description"],
                    "days": 7,
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                print(f"  Content generated successfully!")
                if "data" in data:
                    for item in data["data"][:3]:
                        print(f"    Day {item.get('day', '?')}: {item.get('video_theme', 'N/A')}")
                    if len(data["data"]) > 3:
                        print(f"    ... and {len(data['data']) - 3} more days")
            else:
                print(f"  Error: {resp.status_code} - {resp.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")


# ── Main Entry ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="StoreBoost AI Demo - See the AI growth capabilities in action"
    )
    parser.add_argument("--mock", action="store_true", default=True,
                        help="Run with mock data (default, no API key needed)")
    parser.add_argument("--live", action="store_true",
                        help="Run against live AI service (needs NVIDIA_API_KEY)")
    parser.add_argument("--section", type=str, default="all",
                        choices=["all", "traffic", "content", "review", "growth", "metrics"],
                        help="Run a specific demo section")
    args = parser.parse_args()

    print("\n" + "*" * 60)
    print("  StoreBoost AI - Demo Showcase")
    print("  Let every store use AI-powered growth")
    print("*" * 60)

    if args.live:
        asyncio.run(demo_live_ai_service())
        return

    sections = {
        "traffic": demo_traffic_dashboard,
        "content": demo_content_calendar,
        "review": demo_review_reply,
        "growth": demo_growth_plan,
        "metrics": demo_business_metrics,
    }

    if args.section == "all":
        for func in sections.values():
            func()
    else:
        sections[args.section]()

    print_header("Demo Complete")
    print("\n  Next Steps:")
    print("    1. Start the backend:  cd backend && mvn spring-boot:run")
    print("    2. Start the frontend: cd frontend && npm run dev")
    print("    3. Start AI service:   cd ai-service && python main.py")
    print("    4. Open browser:       http://localhost:5174")
    print()


if __name__ == "__main__":
    main()
