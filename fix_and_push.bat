@echo off
chcp 65001 >nul
cd /d "C:\Users\Lenovo\osrs-guide-site"

echo [1/2] Staging all changes...
git add -A

echo.
echo [2/2] Committing and pushing...
git commit -m "UI update: remove hero, nav black bold, HD images for CTAs and categories, img height 200px"
git push origin main

echo.
echo All done!
pause
