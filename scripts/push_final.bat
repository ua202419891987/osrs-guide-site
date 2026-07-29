@echo off
setlocal EnableDelayedExpansion
cd /d C:\Users\Lenovo\osrs-guide-site

echo ============================================
echo  OSRS Guru - Safe Push (simple v2)
echo  Current HEAD is already at remote latest.
echo ============================================
echo.

echo [1] Revert 6 paid (embargo) files to clean state...
git checkout HEAD -- pt-br/guides/osrs-how-to-make-money-with-zulrah.html pt-br/guides/osrs-hunter-money-making-guide-2026.html pt-br/guides/osrs-slayer-70-to-95-money-makers-2026.html zh/guides/osrs-how-to-make-money-with-zulrah.html zh/guides/osrs-hunter-money-making-guide-2026.html zh/guides/osrs-slayer-70-to-95-money-makers-2026.html
if errorlevel 1 (
  echo REVERT FAILED
  pause
  exit /b 1
)
echo REVERT OK - 6 paid files cleaned
pause
echo.

echo [2] git add -A ...
git add -A
echo ADD OK
pause
echo.

echo [3] Check staged files for any paid (embargo) file...
set FOUND_BAD=0
for %%f in (
  "guides/osrs-how-to-make-money-with-zulrah.html"
  "guides/osrs-wilderness-bosses-guide-2026.html"
  "guides/osrs-gauntlet-meta-changes-2026.html"
  "guides/osrs-hunter-money-making-guide-2026.html"
  "guides/osrs-slayer-70-to-95-money-makers-2026.html"
  "zh/guides/osrs-how-to-make-money-with-zulrah.html"
  "zh/guides/osrs-wilderness-bosses-guide-2026.html"
  "zh/guides/osrs-gauntlet-meta-changes-2026.html"
  "zh/guides/osrs-hunter-money-making-guide-2026.html"
  "zh/guides/osrs-slayer-70-to-95-money-makers-2026.html"
  "pt-br/guides/osrs-how-to-make-money-with-zulrah.html"
  "pt-br/guides/osrs-wilderness-bosses-guide-2026.html"
  "pt-br/guides/osrs-gauntlet-meta-changes-2026.html"
  "pt-br/guides/osrs-hunter-money-making-guide-2026.html"
  "pt-br/guides/osrs-slayer-70-to-95-money-makers-2026.html"
) do (
  git diff --cached --name-only | findstr /x %%f >nul
  if not errorlevel 1 (
    echo BAD: %%f is staged!
    set FOUND_BAD=1
  )
)
if !FOUND_BAD!==1 (
  echo.
  echo PAID FILES DETECTED - aborting, run: git reset HEAD
  pause
  exit /b 1
)
echo GOOD - no paid files staged
pause
echo.

echo [4] Commit...
git commit -m "fix: gold text to black on article pages; money-making card grid"
if errorlevel 1 (
  echo COMMIT FAILED
  pause
  exit /b 1
)
echo COMMIT OK
pause
echo.

echo [5] Push...
git push origin main
if errorlevel 1 (
  echo.
  echo PUSH FAILED - network/proxy. Run manually: git push origin main
  pause
  exit /b 1
)

echo.
echo ============================================
echo  ALL DONE - pushed successfully!
echo ============================================
echo  Check: https://osrsguru.com/money-making.html
echo ============================================
pause
