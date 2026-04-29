# StoreBoost AI - 店长AI增长助手

> 一款帮线下门店用AI做短视频获客 + 客流分析 + 口碑管理的SaaS工具。

---

## 🗂️ 项目结构

```
store-boost-ai/
├── backend/                 # Spring Boot 3 后端（端口8080）
│   ├── src/main/java/com/storeboost/
│   │   ├── entity/           # 实体类（Shop, FootTraffic, ContentCalendar, ReviewAlert, DashboardStats）
│   │   ├── mapper/           # MyBatis-Plus Mapper接口
│   │   ├── service/         # 业务逻辑
│   │   ├── controller/      # REST API
│   │   └── dto/             # 数据传输对象
│   ├── src/main/resources/
│   │   ├── application.yml   # 配置文件
│   │   ├── schema.sql       # 建表语句
│   │   └── init.sql         # 含测试数据的完整初始化
│   └── pom.xml
├── frontend/                # Vue3 前端（端口5174）
│   ├── src/
│   │   ├── App.vue          # 主页面（仪表盘+内容日历+差评管理）
│   │   ├── style.css        # 全局样式
│   │   └── main.js          # 入口
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── start.bat                # 一键启动脚本（Windows）
└── README.md
```

---

## ⚡ 快速启动

### 前置条件

| 软件 | 版本 | 说明 |
|------|------|------|
| JDK | 17+ | 后端运行 |
| Maven | 3.8+ | 后端构建 |
| Node.js | 18+ | 前端运行 |
| MySQL | 8.0+ | 数据库 |

### 启动步骤

```bash
# 1. 双击运行 start.bat（Windows）
# 或手动执行：

# 初始化数据库（用户名root，密码root）
mysql -u root -proot < backend/src/main/resources/init.sql

# 2. 启动后端（端口8080）
cd backend
mvn spring-boot:run

# 3. 启动前端（端口5174）
cd frontend
npm install
npm run dev
```

打开 http://localhost:5174 即可使用。

---

## 🎯 核心功能

### 1. 店铺管理
- 注册店铺（名称/品类/地址/联系方式）
- 支持多店铺切换

### 2. 客流分析
- 手动录入每日客流数据
- 7天趋势折线图（ECharts）
- 进店率统计

### 3. AI内容日历
- 一键生成7天短视频内容计划
- 包含：开场钩子 + 正文 + 行动号召 + 话题标签 + 最佳发布时间
- 支持一键复制脚本

### 4. 差评AI应对
- 差评录入（大众点评/美团/小红书）
- 负面情绪评分（0~1）
- AI生成专业回复话术
- 一键复制回复

### 5. 数据驾驶舱
- 关键指标卡片（本周进店/待发内容/待处理差评/进店率）
- 客流趋势图表
- 内容发布状态
- 差评处理进度

---

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue3 + Vite + Axios + ECharts | 已验证技术 |
| 后端 | Spring Boot 3 + MyBatis-Plus | 复用generic-sys-admin母版 |
| AI服务 | Python FastAPI（端口8000） | 可选接入 |
| 数据库 | MySQL 8 | 5张核心表 |

---

## 📡 API 列表

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | /api/shop/register | 店铺注册 |
| GET | /api/shop/list | 店铺列表 |
| GET | /api/shop/{id} | 店铺详情 |
| POST | /api/foot-traffic | 录入客流数据 |
| GET | /api/foot-traffic/{shopId}/weekly | 客流趋势 |
| POST | /api/content/calendar | 创建内容日程 |
| GET | /api/content/calendar/{shopId} | 内容日历 |
| POST | /api/content/script/generate | AI生成脚本 |
| POST | /api/review/sync | 录入差评 |
| GET | /api/review/alerts/{shopId} | 差评列表 |
| POST | /api/review/reply | AI回复 |
| GET | /api/dashboard/{shopId} | 数据驾驶舱 |

---

## 🚀 开发计划

**Week 1（基础功能）：**
- ✅ 数据库 + 后端 CRUD
- ✅ 前端 Vue 页面
- 🔄 AI 脚本生成接入（FastAPI）

**Week 2（数据+演示）：**
- ⬜ ECharts 数据可视化
- ⬜ 差评 AI 回复功能
- ⬜ 一键复制 + 导出功能

**后续版本：**
- ⬜ Excel 批量导入客流
- ⬜ 店铺口碑排名
- ⬜ AI 增长建议报告

---

## 💡 已复用资产

| 资产 | 用途 |
|------|------|
| generic-sys-admin 母版 | Spring Boot 框架 |
| gov-doc V2.0 Agent架构 | AI 服务层（可升级） |
| ecommerce-ops | 短视频脚本生成逻辑 |
| moderation-platform | 差评 AI 回复 |

---

## 👤 作者

陆阳阳 | 2026-04-29 | 单兵作战版

---

*口号：让每家门店都能用上AI增长能力*