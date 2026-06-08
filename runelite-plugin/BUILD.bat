@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo  OSRS Guru RuneLite Plugin Builder
echo ========================================
echo.

:: Find Java
set JAVA_EXE=
for %%d in (
    "%JAVA_HOME%\bin\java.exe"
    "F:\AI软件相关\5\OpenJDK21U-jdk_x64_windows_hotspot_21.0.11_10\jdk-21.0.11+10\bin\java.exe"
    "C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot\bin\java.exe"
) do (
    if exist %%d (
        set JAVA_EXE=%%d
        goto :found
    )
)

echo [ERROR] Java not found!
echo Please set JAVA_HOME or install JDK 21 from https://adoptium.net/
pause
exit /b 1

:found
echo [OK] Java: %JAVA_EXE%
%JAVA_EXE% -version 2>&1
echo.

:: Set JAVA_HOME from java.exe location
for %%i in ("%JAVA_EXE%\..\..") do set "JDK_HOME=%%~fi"
echo JAVA_HOME=%JDK_HOME%

:: Check Gradle
set GRADLE_EXE=
where gradle >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set GRADLE_EXE=gradle
    goto :build
)

:: Try gradlew
if exist "%~dp0gradlew.bat" (
    set GRADLE_EXE=call "%~dp0gradlew.bat"
    goto :build
)

echo [ERROR] Gradle not found. Install it:
echo   winget install Oracle.JDK.21   (or use chocolatey: choco install gradle)
echo Or download from https://gradle.org/install/
pause
exit /b 1

:build
echo [OK] Gradle ready.
echo.
echo ========================================
echo  Building OSRS Guru Plugin...
echo ========================================
echo.

cd /d "%~dp0"

:: Generate Gradle wrapper if needed
if not exist "gradlew.bat" (
    echo [Step 1/2] Generating Gradle Wrapper...
    call gradle wrapper --gradle-version 7.6 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Gradle wrapper generation failed.
        pause
        exit /b 1
    )
    echo [OK] Wrapper generated.
) else (
    echo [Step 1/2] Gradle Wrapper found, skipping generation.
)

:: Build
echo [Step 2/2] Building plugin JAR...
call gradlew.bat clean fatJar 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo  BUILD FAILED
    echo ========================================
    echo.
    echo Check the errors above. Common fixes:
    echo  1. Make sure JDK 21 is installed
    echo  2. Run: gradle wrapper --gradle-version 7.6
    echo  3. Delete %%USERPROFILE%%\.gradle\caches and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD SUCCESSFUL!
echo ========================================
echo.
set JAR_FILE=
for %%f in (build\libs\*-all.jar) do set JAR_FILE=%%f
if defined JAR_FILE (
    echo Plugin JAR: %~dp0%JAR_FILE%
    for %%f in ("%JAR_FILE%") do echo Size: %%~zf bytes
    echo.
    echo To install locally:
    echo   copy "%JAR_FILE%" "%%USERPROFILE%%\.runelite\externalmanager\"
    echo   Restart RuneLite ^> Settings ^> Plugins ^> search "OSRS Guru AI"
    echo.
    echo To submit to Plugin Hub: see SUBMISSION.md
) else (
    echo JAR file not found in build\libs\. Something went wrong.
)

pause
