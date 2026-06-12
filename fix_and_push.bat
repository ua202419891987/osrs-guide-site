@echo off
echo ===================================================
echo  OSRS Guru - Fix Article Colors ^& Commit All
echo ===================================================

cd /d "C:\Users\Lenovo\osrs-guide-site"

echo.
echo [1/3] Running article color fix script...
"C:\Users\Lenovo\.workbuddy\binaries\python\versions\3.13.12\python.exe" fix_article_colors.py

echo.
echo [2/3] Staging all changes...
git add -A

echo.
echo [3/3] Committing and pushing...
git commit -m "UI优化: 删AI输入框/删Hero Banner/加打赏模块/AI圆形按钮/8版块高清图/版块字体加大/文章深色盒子修复/Chinese改名"
git push origin main

echo.
echo ===================================================
echo  Done! Check osrsguru.com to see the changes.
echo ===================================================
pause
