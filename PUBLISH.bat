@echo off
chcp 65001 >nul
cd /d "C:\Users\Lenovo\osrs-guide-site"

echo ===== Git Status =====
git status --short

echo.
echo ===== Adding all changes =====
git add .

echo.
echo ===== Committing =====
git commit -m "Publish 9 new guides: Sailing 1-99, Sailing Money Making, Agility Training, Hunter Training, Slayer 1-99, Membership Guide, and related updates"

echo.
echo ===== Pushing to GitHub Pages =====
git push origin main

echo.
echo ===== Done =====
pause
