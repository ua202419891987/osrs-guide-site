@echo off
cd /d C:\Users\Lenovo\osrs-guide-site

echo === STEP 1: Stage all already-fixed files on disk ===
echo (NO reset --hard, your 584 edits on disk are kept)
git add -A

echo.
echo === STEP 2: Verify the 5 paid files are NOT staged ===
git diff --cached --name-only > _staged.txt
set "FOUND=0"
for %%F in (
  guides/osrs-how-to-make-money-with-zulrah.html
  guides/osrs-wilderness-bosses-guide-2026.html
  guides/osrs-gauntlet-meta-changes-2026.html
  guides/osrs-hunter-money-making-guide-2026.html
  guides/osrs-slayer-70-to-95-money-makers-2026.html
) do (
  findstr /x "%%F" _staged.txt >nul && echo BAD: %%F is staged & set "FOUND=1"
)
if "%FOUND%"=="0" echo GOOD - no paid files staged

echo.
echo Staged file count:
find /c /v "" < _staged.txt

set /p CONFIRM="Type YES to commit+push: "
if /i not "%CONFIRM%"=="yes" echo ABORTED & del _staged.txt & pause & exit /b 0

echo.
echo === STEP 3: Commit + Push ===
git commit -m "fix: convert gold text to black on article pages; money-making card grid"
if errorlevel 1 echo COMMIT FAILED & del _staged.txt & pause & exit /b 1
git push origin main
if errorlevel 1 echo PUSH FAILED - remote may have new commits, run: git pull --rebase origin main then git push origin main & del _staged.txt & pause & exit /b 1

del _staged.txt
echo.
echo === SUCCESS! ===
pause
