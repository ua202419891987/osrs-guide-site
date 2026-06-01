@echo off
chcp 65001 >nul
cd /d C:\Users\Lenovo\osrs-guide-site

set GIT="C:\Program Files\Git\cmd\git.exe"

echo.
echo ============================================
echo   Checking git status...
echo ============================================
echo.

%GIT% status --short

echo.
echo ============================================
echo   Adding all changes...
echo ============================================
echo.

%GIT% add -A
if %errorlevel% neq 0 (
    echo [FAIL] git add failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Committing...
echo ============================================
echo.

%GIT% commit -m "style: remove white backgrounds - full OSRS warm brown theme"
if %errorlevel% neq 0 (
    echo [WARN] Nothing new to commit, or commit failed
)

echo.
echo ============================================
echo   Pushing to GitHub...
echo ============================================
echo.

%GIT% push origin main
if %errorlevel% neq 0 (
    echo [FAIL] git push failed - check your internet or GitHub login
    pause
    exit /b 1
)

echo.
echo ============================================
echo   SUCCESS! Refresh osrsguru.com in 1-2 min
echo ============================================
echo.

pause
