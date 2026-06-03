# OSRS Guru - 全面修复脚本
# 运行前请确保在 osrs-guide-site 目录下执行

$ErrorActionPreference = "Continue"
$fixedGA4 = 0
$fixedLogo = 0

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  OSRS Guru 网站修复脚本" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. 修复 GA4 ID
Write-Host "`n[1/2] 修复 GA4 Measurement ID..." -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    if ($content -match 'G-5I86091MYV') {
        $newContent = $content -replace 'G-5I86091MYV', 'G-14978162960'
        Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8 -NoNewline
        $fixedGA4++
        Write-Host "  Fixed GA4: $($_.Name)" -ForegroundColor Green
    }
}
Write-Host "  GA4 修复完成: $fixedGA4 个文件" -ForegroundColor Green

# 2. 修复 Logo 缺少 emoji（旧模板文件）
Write-Host "`n[2/2] 修复 Logo emoji..." -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    # 匹配旧版 logo: <a href="..." class="logo">OSRS Guru</a>（前面没有emoji）
    if ($content -match 'class="logo">OSRS Guru</a>') {
        $newContent = $content -replace 'class="logo">OSRS Guru</a>', 'class="logo">⚔️ OSRS Guru</a>'
        Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8 -NoNewline
        $fixedLogo++
        Write-Host "  Fixed Logo: $($_.Name)" -ForegroundColor Green
    }
}
Write-Host "  Logo 修复完成: $fixedLogo 个文件" -ForegroundColor Green

# 3. 验证结果
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  修复汇总" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  GA4 ID 修复: $fixedGA4 个文件"
Write-Host "  Logo emoji 修复: $fixedLogo 个文件"

# 检查是否还有旧ID残留
$remaining = (Get-ChildItem -Path . -Filter "*.html" -Recurse | Where-Object {
    (Get-Content $_.FullName -Raw -Encoding UTF8) -match 'G-5I86091MYV'
}).Count

if ($remaining -eq 0) {
    Write-Host "`n✅ 所有文件 GA4 ID 已正确设置为 G-14978162960" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ 仍有 $remaining 个文件包含旧 ID" -ForegroundColor Red
}

Write-Host "`n下一步：执行 git 提交并推送" -ForegroundColor Cyan
Write-Host "  git add -A"
Write-Host "  git commit -m \"Fix GA4 ID and logo emoji across all pages\""
Write-Host "  git push origin main"
