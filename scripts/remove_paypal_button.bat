@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   Remove green "Support on PayPal" btn
echo   from ALL pages site-wide
echo ========================================
python remove_paypal_button.py
echo.
pause
