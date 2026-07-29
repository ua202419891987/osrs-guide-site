@echo off
cd /d C:\Users\Lenovo\osrs-guide-site

echo === Step 1: Save all current edits to stash ===
git stash

echo === Step 2: Fetch + rebase onto remote main ===
git fetch origin
git rebase origin/main
if errorlevel 1 (echo REBASE FAILED - run: git rebase --abort then git stash pop & pause & exit /b 1)

echo === Step 3: Restore our edits on top of clean remote ===
git stash pop
if errorlevel 1 (echo STASH POP CONFLICT - resolve manually then re-run & pause & exit /b 1)

echo === Step 4: Restore 6 still-modified paid files to clean remote version ===
git checkout -- pt-br/guides/osrs-how-to-make-money-with-zulrah.html pt-br/guides/osrs-hunter-money-making-guide-2026.html pt-br/guides/osrs-slayer-70-to-95-money-makers-2026.html zh/guides/osrs-how-to-make-money-with-zulrah.html zh/guides/osrs-hunter-money-making-guide-2026.html zh/guides/osrs-slayer-70-to-95-money-makers-2026.html

echo === Step 5: Stage everything ===
git add -A

echo === Step 6: Verify NO paid files staged (exact match) ===
set "BAD=0"
for %%F in (
  "guides/osrs-how-to-make-money-with-zulrah.html"
  "guides/osrs-wilderness-bosses-guide-2026.html"
  "guides/osrs-gauntlet-meta-changes-2026.html"
  "guides/osrs-hunter-money-making-guide-2026.html"
  "guides/osrs-slayer-70-to-95-money-makers-2026.html"
  "zh/guides/osrs-how-to-make-money-with-zulrah.html"
  "zh/guides/osrs-wilderness-money-making-2026.html"
  "zh/guides/osrs-corrupted-gauntlet-guide-2026.html"
  "zh/guides/osrs-hunter-money-making-guide-2026.html"
  "zh/guides/osrs-slayer-70-to-95-money-makers-2026.html"
  "pt-br/guides/osrs-how-to-make-money-with-zulrah.html"
  "pt-br/guides/osrs-wilderness-money-making-2026.html"
  "pt-br/guides/osrs-corrupted-gauntlet-guide-2026.html"
  "pt-br/guides/osrs-hunter-money-making-guide-2026.html"
  "pt-br/guides/osrs-slayer-70-to-95-money-makers-2026.html"
) do (git diff --cached --name-only | findstr /x "%%F" >nul && echo BAD: %%F & set "BAD=1")
if "%BAD%"=="0" (echo GOOD - no paid files staged) else (echo BAD - aborting & pause & exit /b 1)

echo === Step 7: Commit + Push ===
git commit -m "fix: gold text to black on article pages; money-making card grid"
git push origin main

echo === DONE ===
pause
