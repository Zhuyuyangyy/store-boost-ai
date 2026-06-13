# StoreBoost AI - Deployment Guide

## Overview

This guide covers deploying StoreBoost AI in development, staging, and production environments.

---

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| JDK | 17+ | Spring Boot backend |
| Maven | 3.8+ | Java build tool |
| Node.js | 18+ | Vue.js frontend |
| Python | 3.10+ | AI service |
| MySQL | 8.0+ | Database |
| Redis | 7.x | Caching & rate limiting (optional) |
| Docker | 24+ | Container deployment (optional) |
| Nginx | 1.24+ | Reverse proxy (optional) |

---

## Development Setup

### 1. Clone and Configure

```bash
git clone <repository-url>
cd store-boost-ai

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### 2. Initialize Database

```bash
mysql -u root -p < backend/src/main/resources/init.sql
```

### 3. Start Services

```bash
# Terminal 1: Backend
cd backend
mvn spring-boot:run

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Terminal 3: AI Service
cd ai-service
pip install -r requirements.txt
export NVIDIA_API_KEY=your-key
python main.py
```

### 4. Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:8080 |
| API Docs | http://localhost:8080/doc.html |
| AI Service | http://localhost:8000/docs |

---

## Docker Deployment

### Using Docker Compose

```bash
cd docker
docker-compose up -d
```

### Manual Docker Build

```bash
# Backend
cd backend
docker build -t store-boost-backend .
docker run -d -p 8080:8080 --name backend store-boost-backend

# AI Service
cd ai-service
docker build -t store-boost-ai .
docker run -d -p 8000:8000 --name ai-service store-boost-ai

# Frontend
cd frontend
docker build -t store-boost-frontend .
docker run -d -p 5174:80 --name frontend store-boost-frontend
```

---

## Production Deployment

### 1. Environment Variables

```bash
# .env production
NVIDIA_API_KEY=prod-key-here
DB_HOST=production-mysql-host
DB_PORT=3306
DB_NAME=store_boost
DB_USER=prod_user
DB_PASSWORD=secure_password
JWT_SECRET=256-bit-secret-key
REDIS_HOST=production-redis-host
```

### 2. Backend Configuration

Edit `backend/src/main/resources/application.yml`:

```yaml
spring:
  datasource:
    url: jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate

jwt:
  secret: ${JWT_SECRET}
  expiration: 86400000
```

### 3. Build for Production

```bash
# Backend
cd backend
mvn clean package -Pproduction
java -jar target/store-boost-backend-1.0.0.jar

# Frontend
cd frontend
npm run build
# Deploy dist/ to Nginx or CDN
```

### 4. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/store-boost-ai/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # AI Service
    location /ai/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Monitoring

### Health Checks

```bash
# Backend
curl http://localhost:8080/actuator/health

# AI Service
curl http://localhost:8000/health
```

### Logs

```bash
# Backend logs
tail -f backend/logs/store-boost.log

# AI Service logs
journalctl -u store-boost-ai -f
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in application.yml or kill existing process |
| Database connection failed | Verify MySQL is running and credentials are correct |
| AI API timeout | Check NVIDIA_API_KEY and network connectivity |
| CORS errors | Verify @CrossOrigin annotation on controllers |

### Debug Mode

```bash
# Backend debug
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"

# AI Service debug
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
```

---

*Last updated: 2026-05-29*
