@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   OSRS Guru - Full Support Module Updater
echo ============================================
echo.
echo This batch will fix ALL guide HTML files:
echo   1. Remove Chinese/Alipay text from support cards
echo   2. Upgrade old "Support on PayPal" buttons to $3/$5/$10/Custom
echo   3. Add inline support hint in article middle
echo.
echo Target: guides\ folder (all *.html)
echo.
pause

:: Try Python first (more reliable)
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found Python. Running Python version...
    python "%~dp0fix_support_python.py"
) else (
    echo Python not found. Falling back to PowerShell...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fix_all_support_v2.ps1"
)

echo.
pause
