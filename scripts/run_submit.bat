@echo off
chcp 65001 >nul
echo ==========================================================
echo  OSRS Guru - 搜索引擎索引提交
echo ==========================================================
echo.

REM 检查 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 检查/安装依赖...
python -m pip install -q google-auth google-api-python-client requests

REM 运行脚本
echo.
echo 🚀 开始提交索引...
echo.
python "%~dp0submit_index.py"

echo.
echo ✅ 完成！
pause
