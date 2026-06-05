@echo off
setlocal enabledelayedexpansion

set "SITE_URL=https://osrsguru.com"
set "ROOT_DIR=%~dp0"

echo === Adding canonical tags to all HTML pages ===
echo.

set /a added=0
set /a skipped=0

REM --- Root files ---
echo --- Root files ---
for %%F in (index.html about.html privacy-policy.html money-making.html skill-training.html quest-guides.html boss-guides.html) do (
    set "FP=%ROOT_DIR%%%F"
    if exist "%%F" (
        findstr /C:"rel=\"canonical\"" "%%F" >nul 2>&1
        if !errorlevel! == 0 (
            echo   SKIP (exists): %%F
        ) else (
            powershell -Command "(Get-Content '%%F' -Raw) -replace '</title>', '</title>\n    <link rel=\"canonical\" href=\"%SITE_URL%/%%F\">' | Set-Content '%%F' -NoNewline"
            if !errorlevel! == 0 (
                echo   ADDED: %SITE_URL%/%%F
                set /a added+=1
            ) else (
                echo   ERROR: %%F
            )
        )
    ) else (
        echo   NOT FOUND: %%F
    )
)

REM --- Guide pages ---
echo.
echo --- Guide pages ---
for %%F in (guides\*.html) do (
    findstr /C:"rel=\"canonical\"" "%%F" >nul 2>&1
    if !errorlevel! == 0 (
        echo   SKIP (exists): %%F
    ) else (
        set "FNAME=%%~nxF"
        powershell -Command "(Get-Content '%%F' -Raw) -replace '</title>', '</title>\n    <link rel=\"canonical\" href=\"%SITE_URL%/guides/%%~nxF\">' | Set-Content '%%F' -NoNewline"
        if !errorlevel! == 0 (
            echo   ADDED: %SITE_URL%/guides/%%~nxF
            set /a added+=1
        ) else (
            echo   ERROR: %%F
        )
    )
)

echo.
echo Done: %added% added, %skipped% skipped.
pause
