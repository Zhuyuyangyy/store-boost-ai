# StoreBoost AI

**AI-Powered Growth Platform for Offline Retail Stores**
**AI驱动的线下门店增长平台**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2-brightgreen.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4fc08d.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479a1.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A SaaS platform that helps brick-and-mortar stores (restaurants, beauty salons, retail) leverage AI for short-video customer acquisition, foot traffic analytics, and online reputation management. Designed so that any store owner -- regardless of marketing expertise -- can use AI-driven growth tools.

一款帮助线下门店（餐饮/美业/零售/健身/宠物）利用AI实现短视频获客、客流分析、口碑管理的SaaS平台。即使不懂运营的店主，也能轻松使用AI驱动的增长工具。

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Benchmarks](#benchmarks)
- [Research](#research)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

---

## Overview

Offline retail stores face a widening digital gap. Foot traffic is fragmented across social platforms, content creation requires skills most store owners lack, and negative reviews can damage reputation before owners even notice. Existing solutions are either too expensive (outsourced agencies at 3000-8000 RMB/month), too generic (template-based tools), or too complex (enterprise platforms designed for large chains).

StoreBoost AI bridges this gap with an integrated system that combines:

1. **AI Content Generation** -- Automatically produces 7-day short-video content calendars with complete scripts, hooks, hashtags, and optimal posting times.
2. **Foot Traffic Analytics** -- Tracks daily passerby-to-entry conversion rates, peak hours, and demographic splits, with trend visualization.
3. **Reputation Management** -- Monitors multi-platform reviews, computes negative sentiment scores, and generates professional AI reply drafts within hours instead of days.
4. **Data Dashboard** -- Aggregates all store metrics into a unified growth cockpit with ECharts visualization.

The AI service layer runs on NVIDIA NIM (deepseek-v4-pro) via FastAPI, while the business layer uses Spring Boot 3 with MySQL and Redis for enterprise-grade reliability.

---

## Key Features

### AI Content Calendar

- One-click generation of 7-day video content plans
- Complete scripts with opening hooks (first 3 seconds), body content, and call-to-action
- Automatic hashtag generation (#storename #category #trending)
- Optimal posting time recommendations based on store history and industry patterns
- Content type variety: seeding, promotional, showcase, storytelling
- Publish status tracking and engagement metrics (views, likes)

### Foot Traffic Analytics

- Daily manual entry of passerby count, entry count, and conversion rate
- Automated conversion rate calculation
- 7-day and 30-day trend line charts
- Peak hour analysis
- Gender ratio and average stay duration tracking
- Excel batch import support

### Review Reputation Management

- Multi-platform review ingestion (Dianping, Meituan, Xiaohongshu, Douyin)
- Negative sentiment scoring algorithm (0-1 scale, keyword + rating + virality weighted)
- AI generates 3 reply versions per review: Apologetic, Explanatory, Corrective
- Risk-level classification: High (respond within 2h), Medium (24h), Low (72h)
- Improvement suggestion generation
- Reply status tracking (pending, replied, adopted)

### Data Dashboard

- Key metric cards: weekly entries, pending content, pending reviews, entry rate
- Traffic trend charts (7-day/30-day)
- Content performance rankings (top 5 by views)
- Conversion funnel: exposure -> click -> entry -> purchase
- Concurrent data aggregation from multiple sources

### Security and Multi-Tenancy

- JWT authentication with Spring Security
- RBAC roles: ADMIN, OWNER, STAFF
- Tenant-level data isolation via `tenant_id` field
- AI API rate limiting per store (20 req/hr free, 100 req/hr paid)
- Operation audit logging

---

## Architecture

```
+------------------------------------------------------------------+
|                          User Layer                               |
|   Store Owner    Staff    Operations    Brand HQ                  |
+-------+----------+-----------+-----------+------------------------+
        |          |           |           |
        v          v           v           v
+------------------------------------------------------------------+
|                    Vue3 SPA (Port 5174)                            |
|   Dashboard  |  Content Calendar  |  Review Alerts  |  Foot Traffic|
|   ECharts + Pinia + Vue Router                                    |
+------------------------------+-----------------------------------+
                               | HTTP/REST
                               v
+------------------------------------------------------------------+
|               Spring Boot 3.2 Backend (Port 8080)                 |
|   ShopController | ContentController | ReviewController           |
|   FootTrafficController | DashboardController | AIController      |
|   [JWT Auth] [RBAC] [Audit Log] [Rate Limit] [Validation]        |
+--------+-----------------+-----------------+---------------------+
         |                 |                 |
         v                 v                 v
+----------------+ +----------------+ +---------------------------+
|  MySQL 8.0     | |  Redis 7.x     | |  FastAPI AI Service       |
|  (Port 3306)   | |  (Port 6379)   | |  (Port 8000)              |
|                | |                | |                           |
|  shop          | |  Session Mgmt  | |  ContentGenerator         |
|  foot_traffic  | |  AI Rate Limit | |  ReviewReplyGen           |
|  content_cal   | |  Dashboard     | |  ViralTitleGen            |
|  review_alert  | |  Cache         | |  GrowthPlanGen            |
|  dashboard     | |                | |         |                 |
|  user          | |                | |         v                 |
|  op_log        | |                | |  NVIDIA NIM API           |
|                | |                | |  deepseek-v4-pro           |
+----------------+ +----------------+ +---------------------------+
```

---

## Tech Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| Frontend | Vue 3 + Composition API | Modern reactive framework |
| Build | Vite 5 | Fast dev server and bundler |
| State | Pinia | Lightweight state management |
| Charts | ECharts 5 | Data visualization (line, bar, pie) |
| HTTP | Axios | Unified interceptor-based client |
| Backend | Spring Boot 3.2 | Enterprise Java framework |
| ORM | MyBatis-Plus 3.5 | Enhanced ORM, no XML configuration |
| Auth | Spring Security + Sa-Token | JWT + RBAC authorization |
| API Docs | Knife4j | Auto-generated API documentation |
| AI Service | FastAPI (Python 3.10+) | Async AI endpoint layer |
| AI Model | NVIDIA NIM / deepseek-v4-pro | Large language model inference |
| Database | MySQL 8.0 | Relational data storage |
| Cache | Redis 7.x | Session, rate limiting, caching |
| Deploy | Docker + Docker Compose | Containerized deployment |
| Proxy | Nginx | Reverse proxy and load balancing |

---

## Quick Start

### Prerequisites

- JDK 17+
- Maven 3.8+
- Node.js 18+
- MySQL 8.0+
- Redis 7.x (optional, for caching/rate limiting)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd store-boost-ai

# Initialize database (default: root/root)
mysql -u root -proot < backend/src/main/resources/init.sql
```

### Start Services

```bash
# Backend (port 8080)
cd backend
mvn spring-boot:run

# Frontend (port 5174)
cd frontend
npm install
npm run dev

# AI Service (port 8000, optional)
cd ai-service
pip install -r requirements.txt
export NVIDIA_API_KEY=your-api-key
python main.py
```

### Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:8080 |
| API Documentation | http://localhost:8080/doc.html |
| AI Service | http://localhost:8000/docs |

### Docker Deployment

```bash
cd docker
docker-compose up -d
```

### Environment Variables

```bash
# AI Service
NVIDIA_API_KEY=your-nvidia-api-key

# Backend (application.yml)
spring.datasource.url=jdbc:mysql://localhost:3306/store_boost
spring.datasource.username=root
spring.datasource.password=root
jwt.secret=your-256-bit-secret
jwt.expiration=86400000
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run smoke tests only
pytest tests/test_smoke.py -v

# Run unit tests only
pytest tests/test_unit.py -v

# Run with coverage report
pytest tests/ -v --cov=ai-service --cov-report=term-missing
```

### Running the Demo

```bash
# Run interactive demo (no API key needed)
python scripts/run_demo.py

# Run specific demo sections
python scripts/run_demo.py --section traffic
python scripts/run_demo.py --section content
python scripts/run_demo.py --section review
```

---

## Project Structure

```
store-boost-ai/
├── backend/                           # Spring Boot 3 backend (port 8080)
│   └── src/main/java/com/storeboost/
│       ├── controller/                # REST API controllers
│       ├── service/                   # Business logic layer
│       ├── mapper/                    # MyBatis-Plus mappers
│       ├── entity/                    # Database entities
│       │   ├── Shop.java
│       │   ├── FootTraffic.java
│       │   ├── ContentCalendar.java
│       │   ├── ReviewAlert.java
│       │   └── DashboardStats.java
│       ├── dto/                       # Data transfer objects
│       ├── config/                    # Configuration classes
│       ├── interceptor/               # Request interceptors
│       ├── security/                  # JWT + RBAC security
│       └── exception/                 # Global exception handling
├── frontend/                          # Vue3 SPA (port 5174)
│   └── src/
│       ├── views/                     # Page components
│       ├── components/                # Reusable components
│       ├── stores/                    # Pinia state stores
│       ├── api/                       # API client wrappers
│       └── router/                    # Vue Router config
├── ai-service/                        # FastAPI AI layer (port 8000)
│   ├── main.py                        # AI service entry point
│   └── prompts/
│       ├── content_calendar.py        # 7-day content prompt
│       ├── review_reply.py            # Review reply prompt
│       ├── viral_title.py             # Viral title prompt
│       └── growth_suggestion.py       # Growth plan prompt
├── docs/                              # Documentation
├── docker/                            # Docker deployment files
├── scripts/                           # Utility scripts
├── tests/                             # Test suite
├── start.bat                          # Windows startup script
├── start.sh                           # Linux startup script
└── README.md
```

---

## Benchmarks

| Metric | Value |
|--------|-------|
| Content Generation | 7-day calendar in <10 seconds |
| Review Reply Generation | 3 versions in <5 seconds |
| Negative Sentiment Detection Accuracy | Keyword + rating heuristic |
| Supported Review Platforms | 4 (Dianping, Meituan, Xiaohongshu, Douyin) |
| Supported Content Categories | Restaurants, Beauty, Retail, Gym, Pet |
| Multi-Tenant Isolation | Per-tenant `tenant_id` field |
| AI Rate Limit | 20 req/hr (free), 100 req/hr (paid) |
| JWT Token Expiration | 24 hours (configurable) |
| Dashboard Concurrent Queries | CompletableFuture parallel aggregation |

---

## Research

### Academic Contributions

| Research Direction | System Contribution | Innovation |
|-------------------|-------------------|------------|
| Multimodal Content Generation | Foot traffic + sentiment -> video scripts | First to integrate physical store data with content generation |
| Spatiotemporal Targeted Delivery | LBS + time + competition -> strategy | Micro-location-based dynamic delivery optimization |
| Multi-Dimensional Reputation Alert | Multi-platform + sentiment + virality | Cross-platform real-time negative review detection |
| Traffic-Conversion Attribution | Short video exposure -> in-store conversion | Content-to-footfall behavioral attribution model |
| AI Topic Selection | Historical data -> intelligent topics | Reinforcement learning-based topic selection from store history |
| Store Competitiveness Profile | Multi-source fusion -> rating | First multi-dimensional offline store competitiveness model |

### Prompt Engineering

The AI service uses structured prompt templates that encode domain expertise:

- **Content Calendar Prompt**: Encodes short-video best practices (hook-first structure, 15-30s format, CTA patterns)
- **Review Reply Prompt**: Generates 3 distinct response strategies calibrated to review severity
- **Viral Title Prompt**: Applies platform-specific viral mechanics (Douyin: emotional hooks, Xiaohongshu: authenticity)
- **Growth Suggestion Prompt**: Synthesizes traffic, content, and review data into actionable recommendations

---

## Roadmap

- [ ] Real-time video analytics integration (Douyin/TikTok API)
- [ ] Automated foot traffic counting via camera integration
- [ ] Multi-store franchise management dashboard
- [ ] A/B testing for content performance optimization
- [ ] WeChat Mini Program frontend
- [ ] Automated review scraping from platforms
- [ ] Predictive foot traffic forecasting with time-series models
- [ ] Multi-language support for international expansion
- [ ] User persona and customer segmentation analysis
- [ ] Marketing strategy recommendation engine
- [ ] Competitor monitoring and benchmarking
- [ ] Conversion funnel optimization with ML models

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

- Issues: [GitHub Issues](https://github.com/yourusername/store-boost-ai/issues)
- Discussions: Open an issue with the `discussion` tag

---

---

## Contributing

We welcome contributions from the community. Here's how to get started:

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest tests/ -v`
5. Run linting: `ruff check .`
6. Submit a pull request

### Code Quality Standards

| Tool | Purpose | Command |
|------|---------|---------|
| Ruff | Python linting & formatting | `ruff check . && ruff format .` |
| Pytest | Test execution | `pytest tests/ -v --cov` |
| Maven | Java build & test | `mvn clean test` |
| ESLint | Frontend linting | `npm run lint` |

### Project Health

| Metric | Status |
|--------|--------|
| Python Tests | 40+ test cases (smoke + unit) |
| CI Pipeline | GitHub Actions (lint + test) |
| Code Coverage | Run `pytest --cov` to check |
| API Documentation | Auto-generated via Knife4j + FastAPI |

---

## Changelog

### v1.1.0 (2026-05-29)
- Added comprehensive test suite (smoke + unit tests)
- Added GitHub Actions CI pipeline
- Added demo script for offline showcasing
- Refactored AI service with DRY helper pattern
- Added deployment guide and business plan documentation

### v1.0.0 (2026-04-29)
- Initial MVP release
- Shop registration and management
- Foot traffic data entry and visualization
- AI content calendar generation (7-day plans)
- Review monitoring and AI reply generation
- Data dashboard with ECharts visualization

---

*Empowering every store with AI-driven growth.*
