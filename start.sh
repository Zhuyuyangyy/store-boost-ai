#!/bin/bash
# store-boost-ai 启动脚本
# 电商运营增长智能体平台 - Spring Boot后端 + AI服务

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "  store-boost-ai - 电商运营增长智能体平台"
echo "=============================================="
echo

# 后端 (Spring Boot)
if [ -d "backend" ] && [ -f "backend/pom.xml" ]; then
    echo "[后端] 启动Spring Boot..."
    if command -v java &>/dev/null; then
        cd backend
        mvn spring-boot:run -q 2>&1 | head -10 &
        echo "[后端] 服务运行于 http://localhost:8080"
    else
        echo "[警告] 未找到Java，跳过后端启动"
    fi
fi

# AI服务 (Python)
if [ -f "ai-service/main.py" ]; then
    echo "[AI服务] 启动AI服务..."
    VENV_DIR="$SCRIPT_DIR/.venv"
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
    pip install -q fastapi uvicorn openai 2>/dev/null
    cd "$SCRIPT_DIR/ai-service"
    python3 main.py &
    echo "[AI服务] 服务运行于 http://localhost:8001"
fi

echo
echo "=============================================="