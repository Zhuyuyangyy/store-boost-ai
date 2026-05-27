# StoreBoost AI - 店长AI增长助手

> 一款帮线下门店用AI做短视频获客 + 客流分析 + 口碑管理的SaaS工具。让每家门店都能用上AI增长能力。

---

## 目录

- [项目背景与痛点](#项目背景与痛点)
- [核心价值主张](#核心价值主张)
- [完整技术架构](#完整技术架构)
- [核心模块详解](#核心模块详解)
- [数据库设计](#数据库设计)
- [AI服务层](#ai服务层)
- [安全与权限体系](#安全与权限体系)
- [部署指南](#部署指南)
- [开发指南](#开发指南)
- [API文档](#api文档)
- [常见问题](#常见问题)

---

## 项目背景与痛点

### 1.1 线下门店面临的数字化困境

在抖音、快手、小红书席卷各行各业的今天，线下门店正面临前所未有的挑战：

| 痛点类型 | 具体表现 | 门店损失 |
|---------|---------|---------|
| 流量碎片化 | 客户从街边经过，但进店率不足20% | 潜在客户流失60%+ |
| 内容生产难 | 老板不懂拍视频，文案写不出来 | 每月少获客200-500人次 |
| 口碑维护滞后 | 差评出现后24小时无法响应 | 评分下降0.5-1.5分 |
| 数据孤岛 | 客流数据、口碑数据、内容数据彼此割裂 | 无法做出科学决策 |
| 投放效率低 | 不知道什么时候投、投什么内容 | 广告浪费30-50% |
| 竞争情报缺失 | 不了解周边竞品动态 | 被动应对，错失先机 |

### 1.2 现有解决方案的不足

**传统方式的问题：**
- 外包代运营：月费用3000-8000元，小店负担不起
- 模板化工具：千篇一律，没有门店特色
- 手工管理：Excel登记，效率低下，数据分散
- 大平台工具：功能复杂，上手难，不贴合门店场景

### 1.3 AI驱动的新范式

StoreBoost AI 重新思考门店增长逻辑，提出"AI+数据+场景"三位一体解决方案：

```
┌──────────────────────────────────────────────────────────┐
│                     StoreBoost AI                        │
│                                                          │
│   ┌────────────┐    ┌────────────┐    ┌────────────┐   │
│   │  客流数据   │ +  │  口碑数据   │ +  │  内容数据   │   │
│   │ (进店率)   │    │ (差评预警)  │    │ (视频脚本)  │   │
│   └─────┬──────┘    └─────┬──────┘    └─────┬──────┘   │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            ▼                             │
│                   ┌────────────────┐                     │
│                   │  AI增长引擎    │                     │
│                   │  • 智能选题    │                     │
│                   │  • 内容生成    │                     │
│                   │  • 口碑应对    │                     │
│                   │  • 趋势预测    │                     │
│                   └────────┬───────┘                     │
│                            ▼                             │
│                   ┌────────────────┐                     │
│                   │  门店增长看板   │                     │
│                   │  进店率↑ 转化↑  │                     │
│                   └────────────────┘                     │
└──────────────────────────────────────────────────────────┘
```

---

## 核心价值主张

### 2.1 学术价值

| 研究方向 | 本系统贡献 | 创新点 |
|---------|----------|--------|
| 多模态内容生成 | 客流+口碑→视频脚本 | 首次将实体客流数据与口碑情感融入内容生成 |
| 时空调量投放 | LBS+时段+竞品→投放策略 | 基于门店微观位置的动态投放优化 |
| 口碑多维预警 | 多平台+情绪+传播→预警 | 融合平台差异的实时负面口碑检测 |
| 客流-转化归因 | 短视频曝光→进店转化链路 | 建立内容曝光到进店的行为归因模型 |
| AI选题决策 | 历史数据→智能选题 | 基于门店历史表现的强化学习选题 |
| 门店竞争力画像 | 多源数据融合→竞争力评级 | 首次提出线下门店多维竞争力模型 |

### 2.2 商业价值

**给门店老板带来的价值：**
- 内容生产效率提升10倍：AI一键生成7天脚本，无需专业团队
- 差评响应时间从48小时缩短到2小时：AI自动生成专业回复
- 进店率平均提升15-30%：基于数据的内容优化
- 每月节省运营成本2000-5000元：替代外包代运营

**给连锁品牌带来的价值：**
- 总部统一管理各门店：多店铺数据看板
- 标准化的内容策略：统一的品牌调性管理
- 区域竞品分析：知己知彼，动态调整

### 2.3 技术价值

- **低门槛**：Vue3前端页面，Spring Boot后端，单人可维护
- **可扩展**：AI服务独立部署，支持替换底层模型
- **安全合规**：JWT鉴权+RBAC+操作日志，满足数据安全要求
- **多租户隔离**：tenant_id字段保证数据隔离，支持SaaS化

---

## 完整技术架构

### 3.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户层 (User Layer)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   门店老板   │  │    店员     │  │   运营人员   │  │   品牌总部   │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
└─────────┼────────────────┼────────────────┼────────────────┼───────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         前端层 (Frontend Layer)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Vue3 单页应用 (localhost:5174)                     │    │
│  │                                                                      │    │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │    │
│  │  │   数据驾驶舱    │  │   内容日历     │  │   差评管理      │           │    │
│  │  │   Dashboard    │  │ ContentCal     │  │  ReviewAlert   │           │    │
│  │  └────────────────┘  └────────────────┘  └────────────────┘           │    │
│  │                                                                      │    │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │    │
│  │  │   客流数据     │  │   店铺管理      │  │   增长报告      │           │    │
│  │  │  FootTraffic   │  │     Shop       │  │  GrowthReport  │           │    │
│  │  └────────────────┘  └────────────────┘  └────────────────┘           │    │
│  │                                                                      │    │
│  │            ECharts 可视化 + Pinia 状态管理 + Vue Router               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────┬────────────────────────────────┘
                                             │ HTTP/REST
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        API网关层 (API Gateway Layer)                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  Spring Boot 3.2 (localhost:8080)                     │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │    │
│  │  │  ShopController  │  │ ContentController │  │ ReviewController  │      │    │
│  │  │  (店铺管理API)   │  │  (内容日历API)    │  │  (差评预警API)   │      │    │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘      │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │    │
│  │  │FootTrafficCtrl  │  │DashboardCtrl    │  │   AIController   │      │    │
│  │  │  (客流分析API)   │  │  (数据驾驶舱API)  │  │   (AI服务API)    │      │    │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘      │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐    │    │
│  │  │                        拦截器栈                                │    │    │
│  │  │   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐ │    │    │
│  │  │   │JWT验证 │  │RBAC鉴权│  │操作日志│  │限流控制│  │参数校验│ │    │    │
│  │  │   └────────┘  └────────┘  └────────┘  └────────┘  └────────┘ │    │    │
│  │  └──────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└────────────────────┬─────────────────────────────┬─────────────────────────┘
                     │                             │
        ┌────────────┴────────────┐   ┌────────────┴────────────┐
        ▼                         ▼   ▼                         ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────────┐
│    MySQL 8.0          │ │    Redis 7.x          │ │    AI 服务层              │
│    (3306)            │ │    (6379)             │ │    (FastAPI 8000)         │
│                     │ │                       │ │                          │
│  ┌────────────────┐  │ │  ┌──────────────────┐  │ │  ┌────────────────────┐  │
│  │  shop          │  │ │  │ 会话管理          │  │ │  │ ContentGenerator   │  │
│  │  foot_traffic  │  │ │  │ /api/auth/*      │  │ │  │ (内容日历生成)     │  │
│  │  content_cal   │  │ │  └──────────────────┘  │ │  └────────────────────┘  │
│  │  review_alert  │  │ │                       │ │  ┌────────────────────┐  │
│  │  dashboard     │  │ │  ┌──────────────────┐  │ │  │ ReviewReplyGen     │  │
│  │  op_log        │  │ │  │ AI限流           │  │ │  │ (差评回复生成)     │  │
│  │  user          │  │ │  │ ratelimit:ai:*   │  │ │  └────────────────────┘  │
│  └────────────────┘  │ │  └──────────────────┘  │ │  ┌────────────────────┐  │
│                     │ │                       │ │  │ ViralTitleGen      │  │
│                     │ │  ┌──────────────────┐  │ │  │ (爆款标题生成)     │  │
│                     │ │  │ 数据缓存          │  │ │  └────────────────────┘  │
│                     │ │  │ dashboard_cache │  │ │  ┌────────────────────┐  │
│                     │ │  └──────────────────┘  │ │  │ GrowthPlanGen      │  │
│                     │ │                       │ │  │ (增长建议生成)     │  │
│                     │ │                       │ │  └────────────────────┘  │
│                     │ │                       │ │           │              │
│                     │ │                       │ │           ▼              │
│                     │ │                       │ │  ┌────────────────────┐  │
│                     │ │                       │ │  │  NVIDIA NIM API    │  │
│                     │ │                       │ │  │  deepseek-v4-pro   │  │
│                     │ │                       │ │  └────────────────────┘  │
└─────────────────────┘ └──────────────────────┘ └──────────────────────────┘
```

### 3.2 技术栈全景

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              技术栈总览                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  【前端层】                                                                  │
│  ├── Vue 3 + Composition API      # 现代化响应式框架                         │
│  ├── Vite 5                       # 极速构建工具                              │
│  ├── Pinia                        # 轻量级状态管理                            │
│  ├── Vue Router 4                 # 客户端路由                                │
│  ├── Axios                        # HTTP客户端（统一拦截器）                  │
│  ├── ECharts 5                   # 数据可视化（折线/柱状/饼图）              │
│  ├── Day.js                      # 日期处理                                 │
│  └── TailwindCSS                 # 原子化CSS（可选）                         │
│                                                                              │
│  【API层】                                                                   │
│  ├── Spring Boot 3.2              # 企业级Java框架                           │
│  │   ├── Spring Security         # 安全框架（JWT + RBAC）                   │
│  │   ├── MyBatis-Plus 3.5        # 增强ORM（无XML配置）                      │
│  │   ├── Sa-Token                # 轻量级权限管理                            │
│  │   ├── Knife4j                  # API文档生成                              │
│  │   ├── EasyExcel               # Excel导入导出                            │
│  │   └── Spring Data Redis       # 缓存/会话/限流                           │
│  └── Redis 7.x                   # 内存数据库                               │
│                                                                              │
│  【AI服务层】                                                                 │
│  ├── FastAPI (Python 3.10+)       # 异步API框架                              │
│  │   ├── httpx                   # 异步HTTP客户端                           │
│  │   ├── Pydantic                # 数据验证                                 │
│  │   └── uvicorn                  # ASGI服务器                              │
│  ├── Prompt Templates            # 提示词模板库                             │
│  │   ├── CONTENT_CALENDAR_PROMPT # 内容日历生成                             │
│  │   ├── REVIEW_REPLY_PROMPT     # 差评回复生成                             │
│  │   ├── VIRAL_TITLE_PROMPT      # 爆款标题生成                             │
│  │   └── GROWTH_SUGGESTION_PROMPT # 增长建议生成                             │
│  └── NVIDIA NIM API              # 大模型调用（deepseek-v4-pro）             │
│                                                                              │
│  【数据层】                                                                   │
│  ├── MySQL 8.0                   # 关系型数据库                              │
│  ├── Redis 7.x                   # 缓存/会话/限流                            │
│  └── 阿里OSS（可选）              # 文件存储                                 │
│                                                                              │
│  【基础设施】                                                                 │
│  ├── Docker + Docker Compose     # 容器化部署                               │
│  ├── Nginx                       # 反向代理/负载均衡                        │
│  └── GitHub Actions              # CI/CD自动化                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 核心模块详解

### 4.1 门店管理模块 (Shop)

**功能描述：** 管理门店基本信息，支持多店铺切换。

**核心能力：**
- 门店注册（名称/品类/地址/联系方式/简介）
- 多店铺列表查询
- 门店详情查看与编辑
- 门店竞争力画像生成

**实体字段：**
```java
Shop {
    id: Long           // 主键
    name: String       // 店名（必填，最大100字符）
    category: String   // 品类（如：餐饮/美业/健身房）
    address: String    // 详细地址
    contact: String    // 联系方式
    description: String // 店铺简介（最大500字符）
    createdAt: DateTime // 创建时间
    updatedAt: DateTime // 更新时间
}
```

**API接口：**
| 方法 | 路径 | 功能 |
|------|------|------|
| POST | /api/shop/register | 注册新门店 |
| GET | /api/shop/list | 获取门店列表 |
| GET | /api/shop/{id} | 获取门店详情 |
| PUT | /api/shop/{id} | 更新门店信息 |
| DELETE | /api/shop/{id} | 删除门店 |
| GET | /api/shop/{id}/profile | 获取竞争力画像 |

---

### 4.2 客流分析模块 (FootTraffic)

**功能描述：** 记录和分析门店客流数据，生成趋势图表。

**核心能力：**
- 每日客流手动录入（路过人数/进店人数/进店率）
- 7天/30天趋势折线图
- 高峰时段分析（peak_hour字段）
- 男女比例统计
- 平均停留时长分析
- 客流预测（基于历史数据）

**实体字段：**
```java
FootTraffic {
    id: Long           // 主键
    shopId: Long       // 门店ID（外键）
    date: LocalDate    // 统计日期
    totalPassers: Int  // 路过总人数
    totalEnter: Int    // 进店总人数
    enterRate: Double  // 进店率（计算得出：totalEnter/totalPassers）
    avgStaySeconds: Int // 平均停留时长（秒）
    maleRatio: Double  // 男性占比
    femaleRatio: Double // 女性占比
    peakHour: String   // 高峰时段（如："11:30,12:30,18:00"）
    createdAt: DateTime // 创建时间
}
```

**数据采集流程：**
```
门店员工每日闭店后录入数据
        │
        ▼
系统自动计算进店率 = 进店人数 / 路过人数 × 100%
        │
        ▼
存储至 foot_traffic 表
        │
        ▼
Dashboard 读取近7天数据 → ECharts 渲染趋势折线图
```

**API接口：**
| 方法 | 路径 | 功能 |
|------|------|------|
| POST | /api/foot-traffic | 录入客流数据 |
| GET | /api/foot-traffic/{shopId}/weekly | 获取近7天趋势 |
| GET | /api/foot-traffic/{shopId}/monthly | 获取近30天趋势 |
| GET | /api/foot-traffic/{shopId}/peak-hours | 获取高峰时段分析 |
| POST | /api/foot-traffic/batch-import | Excel批量导入 |

---

### 4.3 内容日历模块 (ContentCalendar)

**功能描述：** AI一键生成7天短视频内容计划，包含脚本、话题标签、最佳发布时间。

**核心能力：**
- 一键生成7天内容日历
- AI生成完整视频脚本（开场钩子+正文+行动号召）
- 智能推荐最佳发布时间（基于门店历史数据和行业规律）
- 自动生成话题标签（#门店名 #品类 #热点话题）
- 支持一键复制脚本
- 记录发布状态（未发布/已发布）
- 追踪内容效果（播放量/点赞量）

**实体字段：**
```java
ContentCalendar {
    id: Long           // 主键
    shopId: Long       // 门店ID
    planDate: LocalDate // 计划发布日期
    contentType: String // 内容类型（种草/促销/展示/故事）
    videoTheme: String  // 视频主题
    aiScript: Text      // AI生成的完整脚本
    hookText: String    // 开场钩子（吸引眼球的前3秒）
    bodyText: Text      // 正文内容
    ctaText: String     // 行动号召（点赞/关注/到店）
    hashtags: String    // 话题标签（如：#老王家常菜 #红烧肉）
    bestTime: String    // 最佳发布时间（如："12:00"）
    publishStatus: Int  // 发布状态（0=未发布，1=已发布）
    publishedAt: DateTime // 发布时间
    views: Int          // 播放量
    likes: Int          // 点赞量
    createdAt: DateTime // 创建时间
}
```

**AI内容生成流程：**
```
用户点击"AI生成7天内容"
        │
        ▼
前端 POST /api/content/script/generate
        │
        ▼
后端校验店铺信息和品类
        │
        ▼
调用 FastAPI AI服务（端口8000）
        │
        ▼
AI服务构建 Prompt：
- 店铺信息（名称/品类/地址/简介）
- 内容类型要求（种草/促销/展示/故事）
- 行业特点（餐饮/美业/健身房各有策略）
        │
        ▼
请求 NVIDIA deepseek-v4-pro
        │
        ▼
解析JSON响应（处理markdown代码块包裹）
        │
        ▼
更新 content_calendar 表（7条记录）
        │
        ▼
前端渲染7天内容卡片 → 用户可编辑/采纳
```

---

### 4.4 差评预警模块 (ReviewAlert)

**功能描述：** 录入各平台差评，AI自动生成专业回复话术。

**核心能力：**
- 支持多平台录入（大众点评/美团/小红书/抖音）
- 负面情绪评分（0~1，0.8以上为高风险）
- AI生成3个版本回复（道歉型/解释型/整改型）
- 整改建议生成
- 回复状态跟踪（待处理/已回复/已采纳）
- 差评趋势分析

**实体字段：**
```java
ReviewAlert {
    id: Long           // 主键
    shopId: Long       // 门店ID
    platform: String   // 平台（dianping/meituan/xiaohongshu/douyin）
    reviewerName: String // 评论者昵称
    rating: Int        // 评分（1-5星，1-2星为差评）
    negativeScore: Double // 负面情绪得分（0-1）
    content: Text       // 评论内容
    aiSuggestion: Text  // AI整改建议
    aiReply: Text       // AI生成的回复话术
    replyStatus: Int    // 回复状态（0=待处理，1=已回复，2=已采纳）
    replyAdopted: String // 采纳的回复版本
    createdAt: DateTime // 创建时间
}
```

**负面情绪评分算法：**
```
输入：rating（1-5星）, content（评论文本）
输出：negativeScore（0-1）

评分规则：
- rating <= 2 → negativeScore >= 0.7（基础分）
- rating == 1 → negativeScore >= 0.9（最高风险）
- 关键词检测："垃圾"、"骗"、"再也不来" → +0.2
- 传播量检测：高赞评论 → +0.1
- 平台权重：大众点评权重 × 1.2（影响力更大）

最终得分 = min(1.0, 基础分 + 关键词加成 + 传播加成)
```

**AI回复生成流程：**
```
商家手动录入差评（平台+评分+内容）
        │
        ▼
系统计算负面情绪得分
        │
        ▼
判断风险等级：
- 高风险（>=0.8）：2小时内响应提醒
- 中风险（0.5-0.8）：24小时内响应
- 低风险（<0.5）：72小时内响应
        │
        ▼
调用 AI服务生成回复
        │
        ▼
输出3个版本：
- 版本A（诚恳道歉型）：适合服务问题
- 版本B（解释说明型）：适合误解或客观原因
- 版本C（整改承诺型）：适合严重问题，展示改进决心
        │
        ▼
商家选择/编辑 → 采纳 → 记录
```

---

### 4.5 数据驾驶舱模块 (DashboardStats)

**功能描述：** 聚合门店核心数据指标，提供可视化看板。

**核心能力：**
- 关键指标卡片（本周进店/待发内容/待处理差评/进店率）
- 客流趋势图表（7天/30天折线图）
- 内容发布状态（已发布/待发布/草稿）
- 差评处理进度（待处理/处理中/已解决）
- 内容效果排行（播放量TOP5视频）
- 转化漏斗分析（曝光→点击→进店→成交）

**实体字段：**
```java
DashboardStats {
    id: Long           // 主键
    shopId: Long       // 门店ID
    statDate: LocalDate // 统计日期
    contentViews: Int   // 内容播放量
    contentLikes: Int   // 内容点赞量
    contentComments: Int // 内容评论量
    contentShares: Int  // 内容分享量
    newFollowers: Int   // 新增关注
    guideOrders: Int    // 引流订单数
    guideRevenue: Double // 引流成交金额
    createdAt: DateTime // 创建时间
}
```

**Dashboard数据聚合流程：**
```
用户打开Dashboard页面
        │
        ▼
并发查询多个数据源（ CompletableFuture）：
        │
        ├── foot_traffic → 近7天趋势
        ├── content_calendar → 待发布数量 + 已发布效果
        ├── review_alert → 待处理差评数 + 风险分布
        └── dashboard_stats → 累计内容数据
        │
        ▼
聚合计算：
- 进店率趋势 = avg(近7天进店率)
- 内容覆盖率 = 已发布内容数 / 7
- 差评响应率 = 已回复差评数 / 总差评数
- 转化率 = 进店人数 / 内容曝光人数
        │
        ▼
ECharts 渲染多个图表
        │
        ▼
返回完整Dashboard数据
```

---

## 数据库设计

### 5.1 ER图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              数据库 ER 图                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│     ┌──────────────┐                                                        │
│     │     user     │                                                        │
│     ├──────────────┤                                                        │
│     │ id (PK)      │                                                        │
│     │ username     │                                                        │
│     │ password     │                                                        │
│     │ role         │◄──────────────┐                                       │
│     │ tenant_id    │               │ (多租户隔离)                            │
│     │ created_at   │               │                                       │
│     └──────┬───────┘               │                                       │
│            │                       │                                       │
│            │  (tenant_id隔离)      │                                       │
│            ▼                       │                                       │
│     ┌──────────────┐               │                                       │
│     │     shop     │◄──────────────┘                                       │
│     ├──────────────┤                                                        │
│     │ id (PK)      │                                                        │
│     │ tenant_id    │                                                        │
│     │ name         │                                                        │
│     │ category     │                                                        │
│     │ address      │                                                        │
│     │ contact      │                                                        │
│     │ description  │                                                        │
│     │ created_at   │                                                        │
│     └──────┬───────┘                                                        │
│            │                                                               │
│     ┌──────┴───────────────────────────────────────┐                       │
│     │              (一对多关系)                      │                       │
│     ▼                       ▼                       ▼                       │
│ ┌────────────┐       ┌────────────┐         ┌────────────┐                  │
│ │foot_traffic│       │content_cal │         │review_alert│                  │
│ ├────────────┤       ├────────────┤         ├────────────┤                  │
│ │id (PK)     │       │id (PK)     │         │id (PK)     │                  │
│ │shop_id(FK) │       │shop_id(FK) │         │shop_id(FK) │                  │
│ │date        │       │plan_date   │         │platform    │                  │
│ │passers     │       │content_type│         │rating      │                  │
│ │enter       │       │video_theme │         │negative_sc │                  │
│ │enter_rate  │       │ai_script   │         │content     │                  │
│ │peak_hour   │       │hook_text   │         │ai_suggest  │                  │
│ └────────────┘       │best_time   │         │ai_reply    │                  │
│                      │publish_st  │         │reply_status│                  │
│                      │views       │         └────────────┘                  │
│                      │likes       │                                          │
│                      └────────────┘                                          │
│                            │                                                │
│                            ▼                                                │
│                      ┌────────────┐                                         │
│                      │dashboard   │                                         │
│                      │_stats      │                                         │
│                      ├────────────┤                                         │
│                      │id (PK)     │                                         │
│                      │shop_id(FK) │                                         │
│                      │stat_date   │                                         │
│                      │views       │                                         │
│                      │likes       │                                         │
│                      │comments    │                                         │
│                      │shares      │                                         │
│                      │followers   │                                         │
│                      │guide_ord   │                                         │
│                      │guide_rev   │                                         │
│                      └────────────┘                                         │
│                                                                              │
│     ┌──────────────┐                                                        │
│     │ operation_log │                                                        │
│     ├──────────────┤                                                        │
│     │ id (PK)      │                                                        │
│     │ user_id (FK) │                                                        │
│     │ action       │                                                        │
│     │ target_type  │                                                        │
│     │ target_id    │                                                        │
│     │ detail       │                                                        │
│     │ ip           │                                                        │
│     │ created_at   │                                                        │
│     └──────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 表结构说明

| 表名 | 说明 | 记录数估算 | 特点 |
|------|------|-----------|------|
| shop | 门店表 | 一个店铺1条 | 核心表，多个外键关联 |
| foot_traffic | 客流表 | 每店每天1条 | 长期积累，查询频繁 |
| content_calendar | 内容日历表 | 每店每天1条 | AI生成，发布后更新效果 |
| review_alert | 差评预警表 | 按差评数量 | 实时新增，需快速响应 |
| dashboard_stats | 数据看板表 | 每店每天1条 | 聚合数据，缓存优化 |
| user | 用户表 | 按人员数量 | 多租户隔离 |
| operation_log | 操作日志表 | 按操作量 | 审计追溯，只增不减 |

---

## AI服务层

### 6.1 AI服务架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI 服务层架构                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Spring Boot (8080)                    FastAPI (8000)                      │
│        │                                      │                              │
│        │  POST /api/content/script/generate   │                              │
│        │  POST /api/review/reply              │                              │
│        │  POST /api/content/viral-title       │                              │
│        │  POST /api/growth/plan               │                              │
│        │                                      │                              │
│        └──────────────────────────────────────┘                              │
│                           │                                                   │
│                           ▼                                                   │
│              ┌────────────────────────┐                                    │
│              │     Prompt Templates     │                                    │
│              ├────────────────────────┤                                    │
│              │ CONTENT_CALENDAR_PROMPT │  → 生成7天内容日历                 │
│              │ REVIEW_REPLY_PROMPT     │  → 生成差评回复                    │
│              │ VIRAL_TITLE_PROMPT        │  → 生成爆款标题                   │
│              │ GROWTH_SUGGESTION_PROMPT  │  → 生成增长建议                   │
│              └────────────┬─────────────┘                                    │
│                           │                                                   │
│                           ▼                                                   │
│              ┌────────────────────────┐                                    │
│              │    NVIDIA NIM API       │                                    │
│              │    deepseek-v4-pro      │                                    │
│              │    temperature=0.7-0.9 │                                    │
│              │    max_tokens=2048-4096 │                                    │
│              └────────────┬─────────────┘                                    │
│                           │                                                   │
│                           ▼                                                   │
│              ┌────────────────────────┐                                    │
│              │   JSON Response Parser  │                                    │
│              │   (处理markdown包裹)     │                                    │
│              └────────────────────────┘                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Prompt模板设计

**CONTENT_CALENDAR_PROMPT（内容日历生成）：**
```
你是一个专业的短视频运营专家，擅长为线下门店生成7天内容计划。

门店信息：
- 店名：{shop_name}
- 品类：{category}
- 地址：{address}
- 简介：{description}

请为这家门店生成7天的内容日历，每天包括：
1. 内容类型（种草/促销/展示/故事）
2. 视频主题
3. 开场钩子（前3秒，吸引眼球）
4. 正文内容（15-30秒）
5. 行动号召（点赞/关注/到店）
6. 话题标签（3-5个）
7. 最佳发布时间

请以JSON格式输出：
{
  "days": [
    {
      "date": "第1天",
      "content_type": "...",
      "video_theme": "...",
      "hook_text": "...",
      "body_text": "...",
      "cta_text": "...",
      "hashtags": "...",
      "best_time": "..."
    },
    ...
  ]
}
```

**REVIEW_REPLY_PROMPT（差评回复生成）：**
```
你是一个专业的餐饮/服务业客户关系管理专家，擅长处理差评和负面反馈。

差评信息：
- 平台：{platform}
- 评分：{rating}星
- 内容：{content}
- 店铺：{shop_name}（{category}）

请生成3个版本的回复：
1. 诚恳道歉型：适用于服务问题，表示歉意并承诺改进
2. 解释说明型：适用于误解或客观原因，说明情况
3. 整改承诺型：适用于严重问题，展示改进决心

同时给出整改建议，帮助店铺避免类似问题。

请以JSON格式输出：
{
  "replies": [
    {"type": "道歉型", "content": "..."},
    {"type": "解释型", "content": "..."},
    {"type": "整改型", "content": "..."}
  ],
  "suggestion": "..."
}
```

---

## 安全与权限体系

### 7.1 JWT认证流程

```
用户登录
    │
    ▼
POST /api/auth/login { username, password }
    │
    ▼
Spring Security 验证用户密码
    │
    ▼
生成 JWT Token（包含userId, role, tenantId）
    │
    ▼
返回 { token, expiresIn }
    │
    ▼
后续请求携带 Header：
Authorization: Bearer <token>
    │
    ▼
JWT拦截器解析Token → 验证签名 → 提取用户信息 → 设置SecurityContext
    │
    ▼
RBAC权限检查（ADMIN/OWNER/STAFF）
    │
    ▼
通过则执行业务逻辑，否则返回403
```

### 7.2 RBAC权限模型

| 角色 | 权限 | 说明 |
|------|------|------|
| ADMIN | 所有权限 | 系统管理员，可管理所有租户数据 |
| OWNER | 本店铺全权限 | 店铺老板，可管理所有店铺数据 |
| STAFF | 内容+数据权限 | 店员，可查看和编辑内容/数据，不能删除店铺 |

### 7.3 多租户隔离策略

```sql
-- 所有业务查询自动注入 tenant_id 条件
SELECT * FROM shop WHERE tenant_id = :currentTenantId

-- 通过 MyBatis-Plus 拦截器实现，开发者无感知
-- 避免数据泄露风险
```

### 7.4 AI接口限流策略

```sql
-- Redis 实现按店铺维度的限流
KEY: ratelimit:ai:{shop_id}
TTL: 1小时

规则：
- 免费用户：20次/小时
- 付费用户：100次/小时
- 超出返回 429 Too Many Requests
```

---

## 部署指南

### 8.1 环境要求

| 软件 | 版本 | 说明 |
|------|------|------|
| JDK | 17+ | 后端运行必需 |
| Maven | 3.8+ | 后端构建 |
| Node.js | 18+ | 前端运行 |
| MySQL | 8.0+ | 数据库 |
| Redis | 7.x | 缓存/限流（可选） |

### 8.2 快速启动（Windows）

```bash
# 1. 克隆或下载项目后，双击运行 start.bat
# 或手动执行以下步骤：

# 2. 初始化数据库（用户名root，密码root）
mysql -u root -proot < backend/src/main/resources/init.sql

# 3. 启动后端（端口8080）
cd backend
mvn spring-boot:run

# 4. 新开命令行窗口，启动前端（端口5174）
cd frontend
npm install
npm run dev

# 5. 打开浏览器访问
# 前端：http://localhost:5174
# 后端API：http://localhost:8080
# API文档：http://localhost:8080/doc.html
```

### 8.3 Docker部署（推荐）

```yaml
# docker-compose.yml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: store_boost
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/store_boost
      SPRING_REDIS_HOST: redis
    depends_on:
      - mysql
      - redis

  frontend:
    build: ./frontend
    ports:
      - "5174:5174"
    depends_on:
      - backend

  ai-service:
    build: ./ai-service
    ports:
      - "8000:8000"
    environment:
      NVIDIA_API_KEY: ${NVIDIA_API_KEY}

volumes:
  mysql_data:
```

### 8.4 生产环境Nginx配置

```nginx
# /etc/nginx/conf.d/store-boost.conf

upstream backend {
    server 127.0.0.1:8080;
}

upstream ai-service {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # 前端静态资源
    location / {
        root /var/www/store-boost/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # AI服务（内部调用，外部不暴露）
    location /ai/ {
        internal;  # 仅内部访问
        proxy_pass http://ai-service/;
    }
}
```

### 8.5 环境变量配置

```bash
# backend/src/main/resources/application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/store_boost
    username: root
    password: root
  redis:
    host: localhost
    port: 6379

# AI服务
NVIDIA_API_KEY=your-api-key-here

# JWT配置
jwt:
  secret: your-256-bit-secret
  expiration: 86400000  # 24小时
```

---

## 开发指南

### 9.1 项目结构

```
store-boost-ai/
├── backend/                 # Spring Boot 3 后端（端口8080）
│   ├── src/main/java/com/storeboost/
│   │   ├── controller/      # REST API控制器
│   │   ├── service/        # 业务逻辑层
│   │   ├── mapper/         # MyBatis-Plus Mapper
│   │   ├── entity/         # 数据库实体类
│   │   ├── dto/            # 数据传输对象
│   │   ├── config/         # 配置类
│   │   ├── interceptor/    # 拦截器
│   │   ├── security/       # 安全相关
│   │   ├── ai/             # AI服务集成
│   │   └── exception/      # 异常处理
│   ├── src/main/resources/
│   │   ├── application.yml # 配置文件
│   │   ├── schema.sql      # 建表语句
│   │   └── init.sql        # 含测试数据的初始化
│   └── pom.xml
│
├── frontend/                # Vue3 前端（端口5174）
│   ├── src/
│   │   ├── App.vue         # 主页面
│   │   ├── main.js         # 入口
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # Pinia状态管理
│   │   ├── api/            # API封装
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   └── utils/          # 工具函数
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── ai-service/              # Python FastAPI AI层
│   ├── main.py             # 主入口
│   ├── prompts/            # Prompt模板
│   │   ├── content_calendar.py
│   │   ├── review_reply.py
│   │   ├── viral_title.py
│   │   └── growth_suggestion.py
│   └── requirements.txt
│
├── docs/                    # 文档
│   ├── ARCHITECTURE.md     # 系统架构文档
│   ├── PATENT.md           # 专利技术交底书
│   └── API.md              # API文档
│
├── docker/                  # Docker相关
│   ├── docker-compose.yml
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── ai.Dockerfile
│
├── start.bat                # Windows一键启动
├── start.sh                 # Linux启动脚本
└── README.md               # 本文档
```

### 9.2 开发流程

```bash
# 1. 克隆项目
git clone <repository-url>
cd store-boost-ai

# 2. 初始化数据库
mysql -u root -proot < backend/src/main/resources/init.sql

# 3. 启动后端（开发模式，热重载）
cd backend
mvn spring-boot:run

# 4. 启动前端（开发模式，热重载）
cd frontend
npm install
npm run dev

# 5. 启动AI服务（可选）
cd ai-service
pip install -r requirements.txt
python main.py

# 6. 访问
# 前端：http://localhost:5174
# 后端：http://localhost:8080
# API文档：http://localhost:8080/doc.html
# AI服务：http://localhost:8000/docs
```

### 9.3 代码规范

**后端（Java）：**
- 遵循阿里巴巴Java开发规范
- 使用Lombok减少样板代码
- MyBatis-Plus条件构造器替代手写SQL
- 全局异常处理，统一返回格式

**前端（Vue3）：**
- 使用Composition API
- 组件按需引入
- API统一封装在 api/ 目录
- 状态管理使用Pinia

---

## API文档

### 10.1 店铺管理

#### POST /api/shop/register
注册新门店

**请求参数：**
```json
{
  "name": "老王家常菜",
  "category": "餐饮",
  "address": "北京市朝阳区望京街道",
  "contact": "13800138000",
  "description": "20年地道家常菜，人气爆满"
}
```

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 1,
    "name": "老王家常菜",
    "category": "餐饮",
    "address": "北京市朝阳区望京街道",
    "contact": "13800138000",
    "description": "20年地道家常菜，人气爆满",
    "createdAt": "2026-05-17T10:00:00"
  }
}
```

#### GET /api/shop/list
获取门店列表

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": 1,
      "name": "老王家常菜",
      "category": "餐饮",
      "address": "北京市朝阳区望京街道",
      "contact": "13800138000",
      "description": "20年地道家常菜，人气爆满",
      "createdAt": "2026-05-17T10:00:00"
    }
  ]
}
```

### 10.2 客流分析

#### POST /api/foot-traffic
录入客流数据

**请求参数：**
```json
{
  "shopId": 1,
  "date": "2026-05-17",
  "totalPassers": 480,
  "totalEnter": 136,
  "avgStaySeconds": 2600,
  "maleRatio": 55.0,
  "femaleRatio": 45.0,
  "peakHour": "12:00,18:30"
}
```

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 1,
    "shopId": 1,
    "date": "2026-05-17",
    "totalPassers": 480,
    "totalEnter": 136,
    "enterRate": 28.33,
    "avgStaySeconds": 2600,
    "maleRatio": 55.0,
    "femaleRatio": 45.0,
    "peakHour": "12:00,18:30",
    "createdAt": "2026-05-17T22:00:00"
  }
}
```

#### GET /api/foot-traffic/{shopId}/weekly
获取近7天客流趋势

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "shopId": 1,
    "startDate": "2026-05-11",
    "endDate": "2026-05-17",
    "avgEnterRate": 28.08,
    "peakDay": "2026-05-16",
    "trend": [
      {"date": "2026-05-11", "passers": 320, "enter": 85, "enterRate": 26.56},
      {"date": "2026-05-12", "passers": 380, "enter": 102, "enterRate": 26.84},
      {"date": "2026-05-13", "passers": 290, "enter": 78, "enterRate": 26.90},
      {"date": "2026-05-14", "passers": 410, "enter": 115, "enterRate": 28.05},
      {"date": "2026-05-15", "passers": 450, "enter": 128, "enterRate": 28.44},
      {"date": "2026-05-16", "passers": 520, "enter": 148, "enterRate": 28.46},
      {"date": "2026-05-17", "passers": 480, "enter": 136, "enterRate": 28.33}
    ]
  }
}
```

### 10.3 内容日历

#### POST /api/content/calendar
创建内容日程

**请求参数：**
```json
{
  "shopId": 1,
  "planDate": "2026-05-18",
  "contentType": "种草",
  "videoTheme": "招牌红烧肉"
}
```

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 1,
    "shopId": 1,
    "planDate": "2026-05-18",
    "contentType": "种草",
    "videoTheme": "招牌红烧肉",
    "aiScript": "...",
    "hookText": "老板们！这道红烧肉我能吃三碗饭！",
    "bodyText": "今天揭秘我们后厨的秘密...",
    "ctaText": "看完记得点赞关注",
    "hashtags": "#老王家常菜 #红烧肉 #家常菜 #美食",
    "bestTime": "12:00",
    "publishStatus": 0,
    "createdAt": "2026-05-17T10:00:00"
  }
}
```

#### POST /api/content/script/generate
AI生成视频脚本

**请求参数：**
```json
{
  "shopId": 1,
  "shopName": "老王家常菜",
  "category": "餐饮",
  "address": "北京市朝阳区望京街道",
  "description": "20年地道家常菜，人气爆满",
  "days": 7
}
```

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "days": [
      {
        "date": "2026-05-18",
        "content_type": "种草",
        "video_theme": "招牌红烧肉",
        "hook_text": "老板们！这道红烧肉我能吃三碗饭！",
        "body_text": "今天揭秘我们后厨的秘密...",
        "cta_text": "看完记得点赞关注",
        "hashtags": "#老王家常菜 #红烧肉 #家常菜 #美食",
        "best_time": "12:00"
      }
      // ... 共7天
    ]
  }
}
```

### 10.4 差评预警

#### POST /api/review/sync
录入差评

**请求参数：**
```json
{
  "shopId": 1,
  "platform": "dianping",
  "reviewerName": "用户小明",
  "rating": 2,
  "content": "等位等了40分钟，菜上来都凉了，服务态度也不好"
}
```

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 1,
    "shopId": 1,
    "platform": "dianping",
    "reviewerName": "用户小明",
    "rating": 2,
    "negativeScore": 0.80,
    "content": "等位等了40分钟，菜上来都凉了，服务态度也不好",
    "aiSuggestion": "建议：主动联系顾客致歉，提供下次消费优惠补偿；同时优化高峰期排队管理",
    "aiReply": "非常抱歉给您带来不好的体验，我们是20年老店...",
    "replyStatus": 1,
    "createdAt": "2026-05-17T14:30:00"
  }
}
```

#### GET /api/review/alerts/{shopId}
获取差评列表

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total": 2,
    "pending": 1,
    "replied": 1,
    "alerts": [
      {
        "id": 1,
        "platform": "dianping",
        "reviewerName": "用户小明",
        "rating": 2,
        "negativeScore": 0.80,
        "content": "等位等了40分钟，菜上来都凉了，服务态度也不好",
        "replyStatus": 1,
        "createdAt": "2026-05-17T14:30:00"
      },
      {
        "id": 2,
        "platform": "meituan",
        "reviewerName": "吃货张三",
        "rating": 1,
        "negativeScore": 0.95,
        "content": "点的红烧肉明显是预制菜，跟图片差太多，坑人！",
        "replyStatus": 0,
        "createdAt": "2026-05-17T16:00:00"
      }
    ]
  }
}
```

#### POST /api/review/reply
AI生成差评回复

**请求参数：**
```json
{
  "platform": "dianping",
  "rating": 2,
  "content": "等位等了40分钟，菜上来都凉了，服务态度也不好",
  "category": "餐饮",
  "shopName": "老王家常菜"
}
```

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "replies": [
      {"type": "道歉型", "content": "非常抱歉给您带来不好的体验..."},
      {"type": "解释型", "content": "感谢您的反馈，关于等位问题..."},
      {"type": "整改型", "content": "您反馈的问题我们高度重视..."}
    ],
    "suggestion": "建议：主动联系顾客致歉，提供下次消费优惠补偿；同时优化高峰期排队管理"
  }
}
```

### 10.5 数据驾驶舱

#### GET /api/dashboard/{shopId}
获取数据驾驶舱

**响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "shopId": 1,
    "shopName": "老王家常菜",
    "statDate": "2026-05-17",
    "metrics": {
      "weeklyEnter": 792,
      "avgEnterRate": 28.08,
      "pendingContent": 5,
      "pendingReviews": 1,
      "totalViews": 12580,
      "totalLikes": 892
    },
    "trafficTrend": [
      {"date": "2026-05-11", "enterRate": 26.56},
      {"date": "2026-05-12", "enterRate": 26.84}
      // ... 7天数据
    ],
    "contentStatus": {
      "published": 2,
      "pending": 5
    },
    "reviewStatus": {
      "total": 2,
      "pending": 1,
      "replied": 1
    }
  }
}
```

---

## 常见问题

### Q1: 启动报数据库连接错误？
```bash
# 检查MySQL是否运行
mysql -u root -proot -e "SHOW DATABASES;"

# 检查数据库是否存在
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS store_boost;"

# 重新初始化
mysql -u root -proot < backend/src/main/resources/init.sql
```

### Q2: AI功能无法使用？
```bash
# 检查AI服务是否启动
curl http://localhost:8000/health

# 检查NVIDIA API KEY
# 在 ai-service/.env 文件中配置
NVIDIA_API_KEY=your-api-key-here
```

### Q3: 前端页面空白？
```bash
# 检查Node版本（需要18+）
node -v

# 重新安装依赖
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Q4: 如何清空所有数据？
```bash
# 登录MySQL执行
mysql -u root -proot
DROP DATABASE store_boost;
CREATE DATABASE store_boost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 重新初始化
mysql -u root -proot < backend/src/main/resources/init.sql
```

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-04-29 | 初始版本发布 |
| v1.1 | 2026-05-17 | 增强README，添加专利文档 |

---

## 贡献者

**作者：陆阳阳**
- 邮箱：luyangyang@example.com（示例）
- 日期：2026-04-29

**贡献方式：**
- 提交Issue：发现Bug或功能建议
- 提交PR：修复问题或添加功能
- 文档改进：完善文档或翻译

---

## 许可协议

本项目采用 MIT 许可协议开源，您可以自由使用、修改和分发本项目。

---

## 联系方式

- 项目主页：https://github.com/yourusername/store-boost-ai
- 问题反馈：https://github.com/yourusername/store-boost-ai/issues
- 技术讨论：请提交Issue并添加「discussion」标签

---

*口号：让每家门店都能用上AI增长能力*