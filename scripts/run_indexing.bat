@echo off
title OSRS Guru - Google Indexing Submit
echo ============================================
echo   OSRS Guru - Google Indexing Submit
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
pip install --user google-auth-oauthlib google-auth requests --quiet

if %errorlevel% neq 0 (
    echo Retrying without --user...
    pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client --quiet
)

echo.
echo Starting Google Indexing submission...
echo A browser window should open for you to log in to Google.
echo.
cd /d "%~dp0"

REM === Clash Proxy (port 7897) ===
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897
echo Proxy enabled: %HTTP_PROXY%
echo.

python submit_index_oauth.py

echo.
echo ============================================
echo Press any key to close this window...
pause >nul
