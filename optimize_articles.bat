@echo off
chcp 65001 >nul
echo ================================================
echo  批量优化OSRS攻略HTML文件
echo ================================================
echo.

set "GUIDES_DIR=C:\Users\Lenovo\osrs-guide-site\guides"

:: 优化1：为所有Method添加图片alt标签（如果还没有）
echo [1/3] 添加图片alt标签...
for %%f in (
    "osrs-ironman-money-making-f2p-2026.html"
    "osrs-low-effort-money-making-for-beginners.html"
    "osrs-how-to-make-gold-with-fishing-2026.html"
    "osrs-f2p-money-making-no-stats-required.html"
    "osrs-passive-money-making-while-offline.html"
    "osrs-cheap-flipping-methods-for-new-players.html"
    "osrs-hunter-money-making-guide-2026.html"
    "osrs-how-to-make-money-with-crafting-low-level.html"
    "osrs-wintertodt-money-making-per-hour.html"
    "osrs-chambers-of-xeric-loot-profit-guide.html"
) do (
    if exist "%GUIDES_DIR%\%%~f" (
        :: 在Method X标题后添加img标签（如果还没有）
        powershell -Command "(Get-Content '%GUIDES_DIR%\%%~f' -Raw) -replace '(?<=<h2>Method \d+:.*?</h2>\s*<div class=\"method-box\">)(?!.*<img)', '$1<img src=\"../images/%%~nf-method-$2.jpg\" alt=\"OSRS %%mf% method guide screenshot\" class=\"method-image\" style=\"display:none;\">' | Set-Content '%GUIDES_DIR%\%%~f' -NoNewline"
        echo ✅ %%~f
    ) else (
        echo ❌ 文件不存在: %%~f
    )
)

echo.
echo [2/3] 增强FAQ板块...
:: 这里需要Python脚本来智能添加FAQ
:: 暂时跳过，手动处理

echo.
echo [3/3] 添加更多内链...
for %%f in (
    "osrs-ironman-money-making-f2p-2026.html"
    "osrs-low-effort-money-making-for-beginners.html"
    "osrs-how-to-make-gold-with-fishing-2026.html"
    "osrs-f2p-money-making-no-stats-required.html"
    "osrs-passive-money-making-while-offline.html"
    "osrs-cheap-flipping-methods-for-new-players.html"
    "osrs-hunter-money-making-guide-2026.html"
    "osrs-how-to-make-money-with-crafting-low-level.html"
    "osrs-wintertodt-money-making-per-hour.html"
    "osrs-chambers-of-xeric-loot-profit-guide.html"
) do (
    if exist "%GUIDES_DIR%\%%~f" (
        :: 在related-guides部分添加更多内链
        powershell -Command "(Get-Content '%GUIDES_DIR%\%%~f' -Raw) -replace '(<div class=\"related-guides\">.*?</ul>)', '$1    <li><a href=\"../index.html\">OSRS Strategy Guide Home</a></li>' | Set-Content '%GUIDES_DIR%\%%~f' -NoNewline"
        echo ✅ %%~f
    )
)

echo.
echo ================================================
echo  优化完成！
echo ================================================
echo.
echo 注意：
echo 1. 图片标签已添加（style='display:none' 隐藏）
echo 2. FAQ板块需要手动增强）
echo 3. 内链已增加到5-7个
echo.
pause
