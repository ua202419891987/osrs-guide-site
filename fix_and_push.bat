@echo off
chcp 65001 >nul
echo ===== OSRS Guru - Git Push =====
echo.

cd /d "C:\Users\Lenovo\osrs-guide-site"

echo [1/3] Staging all changes...
git add -A

echo [2/3] Committing...
git commit -m "Giscus community forum + index image fixes"

echo [3/3] Pushing to GitHub Pages...
git push origin main

echo.
echo ===== All done! =====
echo Pages will be live in ~30 seconds.
pause
