@echo off
chcp 65001 >nul
cd /d C:\Users\Lenovo\osrs-guide-site

python push_beginner_guides.py
if %errorlevel% neq 0 (
    echo.
    echo [FAIL] 推送失败，请看上方错误信息
    pause
    exit /b 1
)

echo.
echo [DONE] 推送完成
pause
