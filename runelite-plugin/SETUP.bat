@echo off
echo ========================================
echo  OSRS Guru RuneLite Plugin - One-Click Setup
echo ========================================
echo.

:: Check Java
echo [1/3] Checking Java...
java -version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Java NOT FOUND. Please install JDK 11+:
    echo https://adoptium.net/download/
    echo.
    pause
    exit /b 1
)
echo Java OK.

:: Check Gradle, install if needed
echo.
echo [2/3] Checking Gradle...
where gradle >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Gradle not found. Installing via Chocolatey...
    where choco >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Chocolatey not found. Please install it first:
        echo https://chocolatey.org/install
        echo Or install Gradle manually: https://gradle.org/install/
        pause
        exit /b 1
    )
    choco install gradle -y
)
echo Gradle OK.

:: Build
echo.
echo [3/3] Building plugin...
call gradle clean fatJar
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo BUILD FAILED. Check error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD SUCCESSFUL!
echo ========================================
echo.
echo Plugin JAR: build\libs\osrsguru-runelite-plugin-1.0.0-all.jar
echo.
echo To install locally:
echo   copy build\libs\*-all.jar %USERPROFILE%\.runelite\externalmanager\
echo   Restart RuneLite -> Settings -> Plugins -> search "OSRS Guru AI"
echo.
echo To submit to Plugin Hub, see SUBMISSION.md
echo.
pause
