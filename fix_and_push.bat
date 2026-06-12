@echo off
chcp 65001 >nul
cd /d "C:\Users\Lenovo\osrs-guide-site"

echo [1/3] Fixing article colors...
python fix_article_colors.py
if %errorlevel% neq 0 (echo WARNING: Python script had errors, continuing...)

echo.
echo [2/3] Staging all changes...
git add -A

echo.
echo [3/3] Committing and pushing...
git commit -m "UI update: nav font black 1.5x, delete AI banner, delete hero banner, add support card, AI round button, HD images, article dark box fix, Chinese rename"
git push origin main

echo.
echo All done!
pause
