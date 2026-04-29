# StoreBoost AI - 店长AI增长助手

## 1. Concept & Vision

帮助线下门店（餐饮/美业/零售）用AI实现获客增长的SaaS工具。
核心价值：让不懂运营的店主也能轻松生成内容、管理客流、改善口碑。

**第一句话介绍**：一款帮线下门店用AI做短视频获客 + 客流分析 + 口碑管理的工具。

---

## 2. 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue3 + Vite + Axios + ECharts | 已有母版可复用 |
| 后端 | Spring Boot 3 + MyBatis-Plus | 已有generic-sys-admin母版 |
| AI服务 | Python FastAPI（端口8000） | 复用gov-doc V2.0 Agent架构 |
| 数据库 | MySQL 8 | 单机部署 |
| 存储 | 阿里OSS（可选） | MVP阶段先用本地存储 |

---

## 3. 数据库设计（5张表）

### shop 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 自增 |
| name | VARCHAR(100) | 店名 |
| category | VARCHAR(50) | 品类：餐饮/美业/零售/健身房/宠物 |
| address | VARCHAR(255) | 地址 |
| contact | VARCHAR(50) | 联系方式 |
| created_at | DATETIME | 注册时间 |

### foot_traffic 表（客流）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | |
| shop_id | BIGINT FK | |
| date | DATE | |
| total_passers | INT | 经过人数 |
| total_enter | INT | 进店人数 |
| enter_rate | DECIMAL(5,2) | 进店率 |
| avg_stay_seconds | INT | 平均停留 |
| male_ratio | DECIMAL(5,2) | 男性占比 |
| female_ratio | DECIMAL(5,2) | 女性占比 |
| peak_hour | VARCHAR(50) | 高峰时段 |

### content_calendar 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | |
| shop_id | BIGINT FK | |
| plan_date | DATE | |
| content_type | VARCHAR(30) | 种草/促销/展示/热点 |
| video_theme | VARCHAR(200) | 视频主题 |
| ai_script | TEXT | AI生成脚本 |
| publish_status | TINYINT | 0未发 1已发 |
| published_at | DATETIME | |

### review_alert 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | |
| shop_id | BIGINT FK | |
| platform | ENUM | dianping/meituan/xiaohongshu |
| negative_score | DECIMAL(5,2) | 负面得分 |
| ai_suggestion | TEXT | AI整改建议 |
| ai_reply | TEXT | AI回复话术 |
| reply_status | TINYINT | 0未回复 1已回复 |
| created_at | DATETIME | |

### dashboard_stats 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | |
| shop_id | BIGINT FK | |
| stat_date | DATE | |
| views | INT | 播放量 |
| likes | INT | 点赞 |
| comments | INT | 评论 |
| orders | INT | 引导订单 |
| revenue | DECIMAL(10,2) | 引导营收 |

---

## 4. 后端API（Spring Boot 端口8080）

```
POST /api/shop/register              店铺注册
GET  /api/shop/{id}                  店铺信息
POST /api/foot-traffic               上传客流数据
GET  /api/foot-traffic/{shopId}/weekly  本周客流趋势
POST /api/content/calendar            创建内容日历
GET  /api/content/calendar/{shopId}  获取日历
POST /api/review/sync                录入差评
GET  /api/review/alerts/{shopId}     差评列表
POST /api/review/reply               AI回复
GET  /api/dashboard/{shopId}         数据驾驶舱
```

---

## 5. AI服务（FastAPI 端口8000）

```
POST /api/generate-content   输入店铺信息 → 输出7天内容日历
POST /api/generate-reply    输入差评内容 → 输出AI回复话术
POST /api/generate-plan     输入统计数据 → 输出增长建议
```

MVP阶段：单Agent串行，不做多Agent编排。

---

## 6. MVP功能范围（第一版）

✅ 店铺注册（名字+品类+地址）
✅ 手动录入本周客流数据
✅ AI生成7天视频内容日历（点击按钮）
✅ 查看生成的文案脚本
✅ 差评录入，AI给出整改建议
✅ 数据看板（客流趋势折线图 + 内容发布状态）
✅ 一键复制脚本到剪贴板

---

## 7. 两周排期

**Week 1（基础功能）**
- Day 1-2: 建库 + 后端CRUD（店铺/日历/差评）
- Day 3-4: 前端店铺管理页面 + 内容日历页面
- Day 5-7: AI Agent接入，完成脚本生成

**Week 2（数据+演示）**
- Day 8-9: 客流数据页面 + 简易看板
- Day 10-11: 差评监控 + AI回复功能
- Day 12-13: ECharts数据可视化（客流趋势/内容进度/差评统计）
- Day 14: 打包部署 + 找真实商家试用

---

## 8. 已复用资产

| 资产 | 直接用到 |
|------|---------|
| generic-sys-admin（SpringBoot母版） | 后端框架，直接clone |
| gov-doc V2.0 FastAPI Agent | AI服务层 |
| ecommerce-ops（多平台文案） | 短视频脚本生成逻辑 |
| moderation-platform（合规审核） | 差评AI回复 |

---

*Created: 2026-04-29*
*Status: In Progress*