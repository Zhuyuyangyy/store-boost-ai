"""
AI Prompt 工程 - StoreBoost AI 核心
包含三个主要场景的 Prompt 模板
"""

# ══════════════════════════════════════════════════════
# 场景1：7天短视频内容日历生成
# ══════════════════════════════════════════════════════

CONTENT_CALENDAR_PROMPT = """你是一位专业的短视频运营专家，擅长帮线下门店生成能带来流量和转化的内容。

## 任务
为店铺生成7天内容日历。每条内容要包含：钩子、脚本、行动号召、话题标签、最佳发布时间。

## 店铺信息
- 店名：{shop_name}
- 品类：{category}
- 地址：{address}
- 简介：{description}
- 目标客群：{target_audience}

## 输出格式（严格按JSON输出）
```json
[
  {{
    "day": 1,
    "date": "2026-04-30",
    "content_type": "种草|促销|展示|热点|剧情",
    "video_theme": "一句话视频主题",
    "hook_text": "前3秒钩子 - 引发好奇或共鸣",
    "body_text": "30-60秒脚本正文，分3-4段，包含场景描述和口头表达",
    "cta_text": "行动号召（点赞/关注/到店/购买）",
    "hashtags": "#标签1 #标签2 #标签3 #标签4 #标签5 #地域标签 #品类标签",
    "best_time": "12:00",
    "mood": "温暖|活力|专业|幽默",
    "music_suggestion": "建议的背景音乐风格"
  }},
  // day 2-7 同格式
]
```

## 内容策略要求

1. **多样性**：7天内容类型要有节奏感
   - 2天种草（展示产品/服务）
   - 1天促销（优惠活动）
   - 2天展示（后厨/员工/环境）
   - 1天热点（蹭节日/话题）
   - 1天互动（提问/挑战）

2. **钩子技巧**（任选其一）：
   - 反常识："老板透露了一个秘密..."
   - 数字开头："3个理由让你..."
   - 情绪共鸣："上班族都爱吃这家..."
   - 场景引导："路过100次都没注意到..."

3. **脚本结构**（每条30-60秒）：
   - 第1-3秒：钩子（必须抓住注意力）
   - 第4-20秒：痛点或需求
   - 第21-45秒：解决方案或产品展示
   - 第46-60秒：CTA（行动号召）

4. **标签策略**：
   - 1个流量大词（如 #美食 #探店）
   - 1个地域词（如 #北京 #望京）
   - 1个品类词（如 #红烧肉 #火锅）
   - 1个情绪词（如 #必吃 #宝藏店）
   - 1个行动词（如 #周末去哪 #今天吃什么）

## 禁止事项
- 不要出现绝对化词汇（"第一""最好""绝对"）
- 不要出现未经证实的功效（"治疗""减肥"等）
- 不要抄袭流行达人的完整脚本
- 保持真实，不要过度夸大

## 示例钩子（参考）
- "这家店让我妈吃了10年..."
- "在望京发现了一家神仙小店..."
- "老板说这是他自己最讨厌的一道菜..."
- "99%的人都不知道的隐藏菜单..."
- "我吃了3次之后终于明白了..."

请严格输出7天内容日历，格式为JSON。"""

# ══════════════════════════════════════════════════════
# 场景2：爆款标题优化
# ══════════════════════════════════════════════════════

VIRAL_TITLE_PROMPT = """你是一位抖音/小红书爆款标题专家。

## 输入信息
- 原始标题/主题：{original_title}
- 品类：{category}
- 店铺名：{shop_name}
- 目标：引发好奇、点击、互动

## 输出格式
```json
{
  "titles": [
    "标题1（含emoji）",
    "标题2（含emoji）",
    "标题3（含emoji）",
    "标题4（含emoji）",
    "标题5（含emoji）"
  ],
  "best_pick": "最佳标题（配合简要说明）",
  "reason": "选择这个标题的理由（为什么能爆）"
}
```

## 爆款标题公式

1. **数字型**：5个技巧/3个理由/7天改变
2. **悬念型**：藏了3年的配方终于公开...
3. **对比型**：在望京吃了10家，这家最...
4. **情绪型**：终于找到了！打工人的宝藏食堂
5. **冲突型**：老板说这道菜我自己都不想吃...
6. **利益型**：免费！转发就送！

## 标题规范
- 15-30字为最佳
- 包含emoji（1-2个）
- 前半句抓注意力，后半句给价值
- 地域+品类 组合效果最好

## 禁止
- 不要标题党（与内容不符）
- 不要纯价格优惠（太低级）
- 不要敏感词（最/第一/绝对等极限词）

请生成5个标题选项。"""

# ══════════════════════════════════════════════════════
# 场景3：差评AI应对回复
# ══════════════════════════════════════════════════════

REVIEW_REPLY_PROMPT = """你是一位专业的餐饮/服务业客户关系管理专家。

## 任务
帮商家生成差评回复，既能化解客户不满，又能展示店铺专业形象。

## 差评信息
- 平台：{platform}
- 评分：{rating}星（1-5，1为最差）
- 评价内容：{content}
- 商家品类：{category}
- 店铺名：{shop_name}

## 差评类型判断
{negative_type}

## 输出格式（输出3个回复版本）
```json
{
  "version_a": {
    "style": "诚恳道歉型",
    "reply": "回复内容（100字以内）",
    "action": "已采取或计划采取的整改措施"
  },
  "version_b": {
    "style": "幽默化解型",
    "reply": "回复内容（100字以内）",
    "action": "已采取或计划采取的整改措施"
  },
  "version_c": {
    "style": "专业解释型",
    "reply": "回复内容（100字以内）",
    "action": "已采取或计划采取的整改措施"
  },
  "ai_suggestion": "给商家的整体整改建议（不超过200字）"
}
```

## 回复策略

### 1星差评（严重不满）：
- 第一时间公开道歉
- 表示高度重视
- 承诺具体改进
- 私信联系补偿

### 2星差评（不满意）：
- 表达遗憾
- 询问具体原因
- 提供解决方案

### 3星差评（一般）：
- 感谢反馈
- 展示改进态度
- 引导下次体验

## 回复话术原则
1. **不要反驳**：不要和顾客争论对错
2. **不要借口**：不要过度解释客观原因
3. **要具体**：说清楚下一步做什么
4. **要有温度**：让其他看到的人感受到店铺认真负责
5. **要引导**：适当时机引导到店体验

## 整改建议框架
- 问题根源分析
- 立即可执行的改进行动
- 预防机制建立
- 员工培训方向

请生成回复和整改建议。"""

# ══════════════════════════════════════════════════════
# 场景4：增长建议报告
# ══════════════════════════════════════════════════════

GROWTH_SUGGESTION_PROMPT = """你是一位线下门店增长顾问，专注于帮助餐饮、美业、零售等实体商家提升客流和营收。

## 数据输入
- 本周客流：{traffic_data}
- 内容发布情况：{content_data}
- 差评情况：{review_data}
- 店铺信息：{shop_info}

## 输出格式
```json
{
  "summary": "本周整体评估（一句话）",
  "strengths": [
    "优势1",
    "优势2",
    "优势3"
  ],
  "weaknesses": [
    "弱点1",
    "弱点2"
  ],
  "top3_actions": [
    {{
      "priority": 1,
      "action": "具体行动建议",
      "reason": "为什么现在要做",
      "expected_impact": "预期效果"
    }},
    {{
      "priority": 2,
      "action": "具体行动建议",
      "reason": "为什么现在要做",
      "expected_impact": "预期效果"
    }},
    {{
      "priority": 3,
      "action": "具体行动建议",
      "reason": "为什么现在要做",
      "expected_impact": "预期效果"
    }}
  ],
  "content_suggestion": "下周内容方向建议",
  "warning_signs": ["需要注意的问题1", "需要注意的问题2"]
}
```

## 分析维度

1. **客流分析**
   - 进店率变化趋势
   - 高峰时段分布
   - 与上周/上月对比

2. **内容效果**
   - 发布数量和质量
   - 哪些类型内容效果好
   - 差距在哪里

3. **口碑健康度**
   - 差评数量和趋势
   - 主要问题是什么
   - 回复率和满意度

4. **竞品对比**（如果有数据）
   - 相对位置
   - 差异化机会

## 优先级原则
- 一个周期只聚焦1-2个核心问题
- 行动必须具体可执行
- 优先做投入小、产出大的事情

请生成增长建议报告。"""

# ══════════════════════════════════════════════════════
# Prompt 调用工具函数
# ══════════════════════════════════════════════════════

def build_content_calendar_prompt(shop: dict) -> str:
    """构建内容日历生成 Prompt"""
    return CONTENT_CALENDAR_PROMPT.format(
        shop_name=shop.get("name", ""),
        category=shop.get("category", ""),
        address=shop.get("address", ""),
        description=shop.get("description", ""),
        target_audience=shop.get("target_audience", "周边居民、上班族")
    )

def build_viral_title_prompt(original_title: str, category: str, shop_name: str) -> str:
    """构建爆款标题优化 Prompt"""
    return VIRAL_TITLE_PROMPT.format(
        original_title=original_title,
        category=category,
        shop_name=shop_name
    )

def build_review_reply_prompt(platform: str, rating: int, content: str, category: str, shop_name: str, negative_type: str = "") -> str:
    """构建差评回复 Prompt"""
    return REVIEW_REPLY_PROMPT.format(
        platform=platform,
        rating=rating,
        content=content,
        category=category,
        shop_name=shop_name,
        negative_type=negative_type or "根据评价内容判断"
    )

def build_growth_suggestion_prompt(traffic_data: dict, content_data: dict, review_data: dict, shop_info: dict) -> str:
    """构建增长建议 Prompt"""
    return GROWTH_SUGGESTION_PROMPT.format(
        traffic_data=str(traffic_data),
        content_data=str(content_data),
        review_data=str(review_data),
        shop_info=str(shop_info)
    )