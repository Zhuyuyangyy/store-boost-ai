@echo off
chcp 65001 > nul
echo ========================================
echo   StoreBoost AI 启动脚本
echo ========================================
echo.

:: 检查 MySQL
echo [1/3] 检查 MySQL 服务...
mysql -u root -proot -e "USE store_boost;" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [MySQL] 未检测到 store_boost 数据库，正在初始化...
    mysql -u root -proot < "%~dp0backend\src\main\resources\init.sql"
    echo [MySQL] 数据库初始化完成
) else (
    echo [MySQL] 数据库已就绪
)

:: 启动后端
echo.
echo [2/3] 启动后端（端口8080）...
start "StoreBoost-Backend" cmd /c "cd /d %~dp0backend && mvn spring-boot:run"

:: 等待后端启动
echo 等待后端启动（约30秒）...
timeout /t 30 /nobreak > nul

:: 启动前端
echo [3/3] 启动前端（端口5174）...
cd /d %~dp0frontend
call npm install 2>nul
start "StoreBoost-Frontend" cmd /c "npm run dev"

echo.
echo ========================================
echo   启动完成！
echo   后端: http://localhost:8080
echo   前端: http://localhost:5174
echo ========================================
pause