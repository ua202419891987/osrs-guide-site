# OSRS Guru - Batch Support Module Updater
# Updates support cards + adds inline hint in all guide HTML files

$siteDir = "C:\Users\Lenovo\osrs-guide-site"
$guidesDir = "$siteDir\guides"

# ============ NEW SUPPORT CARD HTML ============
$newCard = @'
<!-- Support Card -->
<div class="support-card" style="margin:32px 0 0 0">
    <div class="support-inner">
        <span class="support-icon">🌿</span>
        <div class="support-text">
            <h3>Buy me a pack of gum &mdash; let&apos;s be friends!</h3>
            <p>I&apos;m a game guide creator dedicated to helping OSRS players level up faster. Every donation goes directly into keeping this site updated with fresh content for the community. Support is always optional &mdash; pay what feels right.</p>
            <div class="support-amounts">
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;amp;business=1530398390@qq.com&amp;amp;item_name=Support+OSRSGuru&amp;amp;amount=3&amp;amp;currency_code=USD&amp;amp;no_shipping=1&amp;amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-btn">$3</a>
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;amp;business=1530398390@qq.com&amp;amp;item_name=Support+OSRSGuru&amp;amp;amount=5&amp;amp;currency_code=USD&amp;amp;no_shipping=1&amp;amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-btn recommended">$5 ★</a>
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;amp;business=1530398390@qq.com&amp;amp;item_name=Support+OSRSGuru&amp;amp;amount=10&amp;amp;currency_code=USD&amp;amp;no_shipping=1&amp;amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-btn">$10</a>
                <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&amp;amp;business=1530398390@qq.com&amp;amp;item_name=Support+OSRSGuru+-+Buy+me+a+pack+of+gum&amp;amp;currency_code=USD&amp;amp;no_shipping=1&amp;amp;return=https://osrsguru.com" target="_blank" rel="noopener" class="support-amount-custom">Custom ✎</a>
            </div>
        </div>
    </div>
</div>
'@

# ============ INLINE SUPPORT HINT HTML ============
$inlineHint = @'

            <div class="inline-support-hint">
                <p>If this guide helped you on your OSRS journey, <strong>consider supporting the author</strong> below &mdash; it keeps this site free and updated for everyone. ❤️</p>
            </div>
'@

# ============ OLD PATTERNS (Regex) ============
# Pattern A: button inside support-inner
$oldA = '(?s)<div\s+class="support-card"[^>]*>\s*<div\s+class="support-inner">\s*<span\s+class="support-icon">[^<]+</span>\s*<div\s+class="support-text">\s*<h3>[^<]+</h3>\s*<p>[^<]+</p>\s*</div>\s*<a\s+href="[^"]*paypal[^"]*"[^>]*class="support-btn[^"]*"[^>]*>[^<]+</a>\s*</div>\s*</div>'
# Pattern B: button outside support-inner
$oldB = '(?s)(?:<!--\s*S[sU]pport\s+C[aA]rd\s*-->\s*)?<div\s+class="support-card"[^>]*>\s*<div\s+class="support-inner">\s*<span\s+class="support-icon">[^<]+</span>\s*<div\s+class="support-text">\s*<h3>[^<]+</h3>\s*<p>[^<]+</p>\s*</div>\s*</div>\s*<a\s+href="[^"]*paypal[^"]*"[^>]*class="support-btn[^"]*"[^>]*>[^<]+</a>\s*</div>'

# Pattern for inserting inline hint before Support Card comment
$supportCommentPattern = '(?s)(\s*)(<!--\s*Support Card\s*-->)'

$files = Get-ChildItem -Path $guidesDir -Filter "*.html"
$total = $files.Count
$cardUpdated = 0
$hintAdded = 0

Write-Host "Scanning $total files in guides/..." -ForegroundColor Cyan
Write-Host ""

foreach ($f in $files) {
    $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $name = $f.Name
    $changed = $false

    # Step 1: Update support card
    if ($content -match 'paypal') {
        $newContent = $content -replace $oldA, $newCard
        $newContent = $newContent -replace $oldB, $newCard
        if ($newContent -ne $content) {
            $content = $newContent
            $cardUpdated++
            $changed = $true
        }
    }

    # Step 2: Add inline hint before Support Card comment (if not already present)
    if (-not $content.Contains('inline-support-hint') -and $content -match 'Support Card') {
        $content = $content -replace $supportCommentPattern, "`$1$inlineHint`$2"
        if (-not $changed -and $content -match 'inline-support-hint') {
            $changed = $true
        }
        if ($content -match 'inline-support-hint') { $hintAdded++ }
    }

    if ($changed) {
        [System.IO.File]::WriteAllText($f.FullName, $content, [System.Text.Encoding]::UTF8)
        Write-Host "  OK  $name" -ForegroundColor Green
    } else {
        Write-Host "  --  $name" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host ("=" * 55)
Write-Host "Cards updated : $cardUpdated / $total"
Write-Host "Hints added  : $hintAdded / $total"
Write-Host "All done!" -ForegroundColor Cyan
