@echo off
chcp 65001 >nul 2>&1
echo.
echo ================================================
echo   Add "Support on PayPal 💳" to ALL Support Cards
echo ================================================
echo   This will process ~100 HTML files...
echo.

cd /d "C:\Users\Lenovo\osrs-guide-site"
python "scripts\add_paypal_button.py"

echo.
echo ================================================
echo   DONE! You can now: git push origin main
echo ================================================
pause
