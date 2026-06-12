@echo off
chcp 65001 >nul
cd /d "C:\Users\Lenovo\osrs-guide-site"

echo [1/2] Staging all changes...
git add -A

echo.
echo [2/2] Committing and pushing...
git commit -m "4 fixes: logo swords+purple, nav black+white, HD images deduped, community forum page"
git push origin main

echo.
echo All done!
pause
