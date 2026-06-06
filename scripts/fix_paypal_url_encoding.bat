@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   Fix double-encoded PayPal URLs
echo   &amp;amp; -> &amp;
echo ========================================
python fix_paypal_url_encoding.py
echo.
pause
