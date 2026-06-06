# Comprehensive Support Card Fixer v2
# Fixes: 1) Remove Chinese/Alipay text, 2) Upgrade old cards to amount buttons, 3) Add inline hint
$guidesDir = "C:\Users\Lenovo\osrs-guide-site\guides"

# Read new card from template file
$newCard = Get-Content -Path "$PSScriptRoot\new_card_template.txt" -Raw -Encoding UTF8

# Inline support hint
$inlineHint = @'

            <div class="inline-support-hint">
                <p>If this guide helped you on your OSRS journey, <strong>consider supporting the author</strong> below &mdash; it keeps this site free and updated for everyone. ❤️</p>
            </div>
'@

# Pattern A: Remove Chinese payment note from new-format cards
$patternA_RemoveChinese = '(?s)\s*<div class="support-alt-pay">\s*<p>&#127468;&#127463; Chinese users prefer Alipay or WeChat\?.*?</div>\s*'

# Pattern B1: Old format card (support-btn inside support-inner)
$oldPattern_B1 = '(?s)<div\s+class="support-card"[^>]*>\s*<div\s+class="support-inner">\s*<span\s+class="support-icon">[^<]+</span>\s*<div\s+class="support-text">\s*<h3>[^<]+</h3>\s*<p>[^<]+</p>\s*</div>\s*<a\s+href="[^"]*paypal[^"]*"[^>]*class="support-btn[^"]*"[^>]*>[^<]+</a>\s*</div>\s*</div>'

# Pattern for inserting inline hint before Support Card comment
$supportCommentPattern = '(?s)(\s*)(<!--\s*Support Card\s*-->)'

$files = Get-ChildItem -Path $guidesDir -Filter "*.html"
$total = $files.Count
$chineseRemoved = 0
$oldCardUpgraded = 0
$hintAdded = 0
$alreadyGood = 0
$errors = @()

Write-Host "============================================"
Write-Host "  COMPREHENSIVE SUPPORT CARD FIXER v2"
Write-Host "  Total files: $total"
Write-Host "============================================"
Write-Host ""

foreach ($f in $files) {
    $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $name = $f.Name
    $changed = $false
    $actions = @()

    # Step 1: Remove Chinese/Alipay text
    if ($content -match 'Alipay|WeChat|support-alt-pay') {
        $newContent = $content -replace $patternA_RemoveChinese, ''
        if ($newContent.Length -ne $content.Length) {
            $content = $newContent
            $chineseRemoved++
            $changed = $true
            $actions += "RM-CN"
        }
    }

    # Step 2: Upgrade old-format cards ("Support on PayPal" button)
    if ($content -match 'Support on PayPal|class="support-btn') {
        $beforeLen = $content.Length
        $content = $content -replace $oldPattern_B1, $newCard
        if ($content.Length -ne $beforeLen) {
            $oldCardUpgraded++
            $changed = $true
            $actions += "UPG"
        }
    }

    # Step 3: Add inline support hint
    if (-not $content.Contains('inline-support-hint') -and $content -match 'Support Card|support-card') {
        $content = $content -replace $supportCommentPattern, "`$1$inlineHint`$2"
        if ($content.Contains('inline-support-hint')) {
            $hintAdded++
            $changed = $true
            $actions += "HINT"
        }
    }

    if ($changed) {
        try {
            [System.IO.File]::WriteAllText($f.FullName, $content, [System.Text.Encoding]::UTF8)
            Write-Host "  OK  $($name.PadRight(50)) [$($actions -join ' ')]" -ForegroundColor Green
        } catch {
            $errors += "$name : $($_.Exception.Message)"
            Write-Host "  ERR $name" -ForegroundColor Red
        }
    } else {
        if ($content -match 'support-amount-btn' -and $content -match 'inline-support-hint') {
            $alreadyGood++
        } elseif ($content -notmatch 'support-card') {
            Write-Host "  SKIP $name  (no card)" -ForegroundColor DarkGray
        } else {
            Write-Host "  ??   $name  (review!)" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host ("=" * 60)
Write-Host "Chinese removed   : $chineseRemoved"
Write-Host "Old cards upgraded: $oldCardUpgraded"
Write-Host "Inline hints added: $hintAdded"
Write-Host "Already correct   : $alreadyGood"
Write-Host "Errors            : $($errors.Count)"
if ($errors.Count -gt 0) { foreach ($e in $errors) { Write-Host "  ERR: $e" -ForegroundColor Red } }
Write-Host ""
Write-Host "DONE!" -ForegroundColor Cyan
