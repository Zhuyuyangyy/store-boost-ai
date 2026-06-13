# StoreBoost AI 系统架构文档

> 工业级线下门店AI增长SaaS系统

---

## 1. 系统架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                           用户层 (User)                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  老板    │  │  店员    │  │  运营    │  │  管理员  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼────────────┼────────────┼────────────┼─────────────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         前端层 (Frontend)                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Vue3 单页应用 (localhost:5174)              │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐    │   │
│  │  │ Dashboard │ │  内容日历  │ │  差评管理  │ │  客流数据  │    │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘    │   │
│  │                     ECharts 可视化 + 状态管理                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ HTTP / WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API网关层 (API Gateway)                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Spring Boot 3 (localhost:8080)                  │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │   │
│  │  │ShopController│ContentCtrl│ReviewCtrl│FootTrafficCtrl│     │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │                   统一拦截器                          │   │   │
│  │  │   • JWT 鉴权   • RBAC 权限   • 操作日志   • 限流     │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────┬─────────────────┘
                  │                               │
        ┌─────────┴─────────┐           ┌─────────┴─────────┐
        ▼                   ▼           ▼                   ▼
┌───────────────────┐ ┌───────────────┐ ┌───────────────────┐
│   MySQL 8.0       │ │  Redis 7.x    │ │   AI 服务层        │
│   (store_boost)   │ │  (会话/限流)   │ │   (FastAPI 8000)   │
│                   │ │               │ │                   │
│  ┌─────────────┐  │ │  • Token      │ │  ┌─────────────┐  │
│  │  shop       │  │ │  • RateLimit  │ │  │ ContentGen  │  │
│  │  foot_traffic│  │ │  • Cache      │ │  │ ReviewReply │  │
│  │  content_cal│  │ │  • Pub/Sub    │ │  │ GrowthPlan  │  │
│  │  review_alert│  │ └───────────────┘ │  └─────────────┘  │
│  │  dashboard  │  │                   │  ┌─────────────┐  │
│  │  op_log     │  │                   │  │ Prompt库    │  │
│  │  user       │  │                   │  │ (爆款生成)  │  │
│  └─────────────┘  │                   │  └─────────────┘  │
└───────────────────┘                   └───────────────────┘
                                              │
                                              ▼
                                   ┌───────────────────────┐
                                   │  NVIDIA NIM API       │
                                   │  deepseek-v4-pro      │
                                   └───────────────────────┘
```

---

## 2. 技术栈全景

```
前端层
├── Vue 3 + Composition API
├── Vite 5 (构建工具)
├── Pinia (状态管理)
├── Vue Router
├── Axios (HTTP 客户端)
├── ECharts 5 (数据可视化)
└── TailwindCSS (可选)

API层
├── Spring Boot 3.2
│   ├── Spring Security (JWT + RBAC)
│   ├── MyBatis-Plus 3.5 (ORM)
│   ├── Sa-Token (权限管理)
│   ├── Knife4j (API文档)
│   └── EasyExcel (Excel导入导出)
└── Redis (会话 + 限流 + 缓存)

AI服务层
├── FastAPI (异步 Python 服务)
│   ├── httpx (HTTP 客户端)
│   ├── Prompt Templates (4大场景)
│   └── SSE (流式响应)
└── NVIDIA NIM (deepseek-v4-pro)

数据层
├── MySQL 8.0 (主数据库)
├── Redis 7.x (缓存/会话/限流)
└── 阿里OSS (文件存储)

基础设施
├── Docker (容器化)
├── Nginx (反向代理)
└── CI/CD (自动部署)
```

---

## 3. 数据库ER图

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    user     │       │      shop       │       │   foot_traffic  │
├─────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)     │       │ id (PK)         │       │ id (PK)         │
│ username    │◄──┐  │ name            │       │ shop_id (FK)────┼──►shop
│ password    │   │  │ category        │       │ date            │
│ role        │   │  │ address         │       │ total_passers   │
│ tenant_id   │───┘  │ contact         │       │ total_enter     │
│ created_at  │       │ created_at      │       │ enter_rate      │
└─────────────┘       └─────────────────┘       │ peak_hour       │
    │                                           └─────────────────┘
    │ (tenant隔离)
    │                                                │
    ▼                                                │
┌─────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ operation_log│      │ content_calendar│       │  review_alert   │
├─────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)     │       │ id (PK)         │       │ id (PK)         │
│ user_id (FK)│       │ shop_id (FK)────┼──►    │ shop_id (FK)────┼──►shop
│ action      │       │ plan_date       │       │ platform        │
│ target_type │       │ content_type    │       │ rating          │
│ target_id   │       │ video_theme     │       │ content         │
│ detail      │       │ ai_script       │       │ ai_suggestion   │
│ ip          │       │ hook_text       │       │ ai_reply        │
│ created_at  │       │ publish_status  │       │ reply_status    │
└─────────────┘       │ best_time       │       └─────────────────┘
                      └─────────────────┘

              ┌─────────────────┐
              │ dashboard_stats │
              ├─────────────────┤
              │ id (PK)         │
              │ shop_id (FK)────┼──►shop
              │ stat_date       │
              │ content_views   │
              │ guide_orders    │
              │ guide_revenue   │
              └─────────────────┘
```

---

## 4. 核心业务流程

### 4.1 内容生成流程

```
用户点击"AI生成7天内容"
         │
         ▼
前端 POST /api/content/script/generate
         │
         ▼
后端校验权限（RBAC）
         │
         ▼
调用 FastAPI AI服务（端口8000）
         │
         ▼
AI服务解析Prompt模板（CONTENT_CALENDAR_PROMPT）
         │
         ▼
请求 NVIDIA deepseek-v4-pro
         │
         ▼
解析JSON响应 → 更新 content_calendar 表
         │
         ▼
返回前端 → 页面展示7天卡片
```

### 4.2 差评处理流程

```
商家录入差评（手动）
         │
         ▼
POST /api/review/sync
         │
         ▼
计算负面情绪得分（rating ≤ 2 → 0.8高风险）
         │
         ▼
AI服务调用 REVIEW_REPLY_PROMPT
         │
         ▼
生成3个版本回复 + 整改建议
         │
         ▼
商家选择/编辑/采纳
         │
         ▼
operation_log 记录完整操作
```

### 4.3 数据看板流程

```
用户打开Dashboard
         │
         ▼
GET /api/dashboard/{shopId}
         │
         ▼
并发查询：
  • foot_traffic 近7天趋势
  • content_calendar 发布状态
  • review_alert 待处理数量
         │
         ▼
聚合数据 + ECharts 渲染
         │
         ▼
返回仪表盘数据
```

---

## 5. 安全架构

```
请求流程：

Client
  │
  ▼
┌─────────────────┐
│  登录获取 JWT   │ ← 用户名/密码 → JWT Token
└─────────────────┘
  │
  │ Authorization: Bearer <token>
  ▼
┌─────────────────┐
│  Spring Security │ ← JWT解密 + 权限验证
│  拦截器          │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  RBAC 权限检查   │
│  • ADMIN         │ ← 系统管理（用户/店铺）
│  • OWNER         │ ← 店铺老板（全权限）
│  • STAFF         │ ← 店员（内容/数据）
└─────────────────┘
  │
  ▼
┌─────────────────┐
│  操作日志记录   │
│  写入 op_log    │
└─────────────────┘
  │
  ▼
业务逻辑执行
```

---

## 6. 部署架构

```
                        ┌─────────────────────┐
                        │   Nginx (80/443)    │
                        │   SSL证书           │
                        │   反向代理          │
                        └──────────┬──────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │  Vue 前端 (5174)  │  │  Spring Boot     │  │  FastAPI AI      │
   │  静态资源         │  │  (8080)          │  │  (8000)          │
   │                   │  │                   │  │                   │
   │                   │  │  /api/*          │  │  /generate-*     │
   └───────────────────┘  └──────────────────┘  └──────────────────┘
                                    │                    │
                                    ▼                    ▼
                           ┌────────────────┐    ┌────────────────┐
                           │   MySQL 8.0    │    │  Redis 7.x     │
                           │   (3306)       │    │  (6379)        │
                           └────────────────┘    └────────────────┘
```

---

## 7. 多租户隔离策略

```
tenant_id 字段在所有业务表中的隔离方式：

shop 表：
  tenant_id NOT NULL
  店铺创建时绑定到当前用户 tenant_id

数据访问：
  SELECT * FROM shop WHERE tenant_id = :currentTenantId
  （拦截器自动注入，开发者无感知）

优势：
  • 简单高效（不需要复杂 row-level security）
  • 单库多租户（运维简单）
  • 扩展路径清晰（分库分表）
```

---

## 8. 限流策略（Redis）

```
AI 接口限流（按店铺维度）：

key: ratelimit:ai:{shop_id}
value: 计数
ttl: 1小时

规则：
  • 免费用户：20次/小时
  • 付费用户：100次/小时
  • 超出返回 429 Too Many Requests

实现：
  Redis INCR + EXPIRE
  Lua 脚本保证原子性
```

---

## 9. 项目目录结构

```
store-boost-ai/
│
├── backend/
│   └── src/main/java/com/storeboost/
│       ├── controller/        # REST API（店铺/内容/差评/客流/仪表盘）
│       ├── service/          # 业务逻辑
│       ├── mapper/           # MyBatis-Plus Mapper
│       ├── entity/           # 实体类（5张核心表）
│       ├── dto/              # 数据传输对象
│       ├── config/           # 配置类（Redis/Security/WebMvc）
│       ├── interceptor/      # 拦截器（日志/鉴权/限流）
│       ├── security/         # JWT/Sa-Token/RBAC
│       ├── ai/               # AI 服务集成（调用 FastAPI）
│       └── exception/        # 全局异常处理
│
├── frontend/
│   └── src/
│       ├── views/            # 页面（Dashboard/Calendar/Review/Traffic）
│       ├── components/       # 组件（MetricCard/ContentCard/ReviewRow）
│       ├── router/           # Vue Router
│       ├── stores/           # Pinia 状态管理
│       ├── api/              # Axios 封装
│       └── utils/            # 工具函数
│
├── ai-service/                # Python FastAPI AI层（独立微服务）
│   ├── main.py
│   ├── prompts/
│   │   ├── content_calendar.py
│   │   ├── viral_title.py
│   │   ├── review_reply.py
│   │   └── growth_suggestion.py
│   └── bridge/
│       └── nvidia_client.py
│
├── docs/                     # 架构文档
│   ├── ARCHITECTURE.md      # 本文档
│   ├── DATABASE.md          # 数据库设计
│   └── API.md               # API 文档
│
├── docker/
│   ├── docker-compose.yml   # 全量容器编排
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── ai.Dockerfile
│
└── deployment/
    ├── nginx.conf
    └── deploy.sh
```

---

*文档版本：v1.0*
*最后更新：2026-04-29*