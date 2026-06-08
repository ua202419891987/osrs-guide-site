@echo off
title OSRS Guru - Submit 6 NEW Articles
echo ============================================
echo   OSRS Guru - Submit 6 NEW Articles (June 2026)
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3 from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing dependencies...
pip install --user google-auth-oauthlib google-auth requests --quiet 2>nul

echo.
echo Starting Google Indexing submission...
echo A browser may open for you to log in to Google.
echo.
cd /d "%~dp0"

REM === Clash Proxy (port 7897) ===
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897
echo Proxy enabled: %HTTP_PROXY%
echo.

python submit_6_new_articles.py

echo.
echo ============================================
echo Press any key to close this window...
pause >nul
