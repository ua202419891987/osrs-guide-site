@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Install Gradle + Build Plugin
echo ========================================
echo.

:: Accept zip path (drag-drop or first argument)
set ZIP=%1
if "%ZIP%"=="" (
    echo Please drag the gradle-8.5-bin.zip file onto this script.
    echo Or run: INSTALL_GRADLE.bat "F:\AI智能体6\gradle-8.5-bin.zip"
    pause
    exit /b 1
)

echo ZIP: %ZIP%

:: Extract to user home
set "GRADLE_HOME=%USERPROFILE%\gradle"
echo Extracting to %GRADLE_HOME%...

if exist "%GRADLE_HOME%\gradle-8.5" (
    echo Gradle already extracted, skipping.
    goto :setpath
)

powershell -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '%GRADLE_HOME%' -Force" 2>&1

if exist "%GRADLE_HOME%\gradle-8.5\bin\gradle.bat" (
    echo [OK] Gradle extracted successfully.
) else (
    echo [ERROR] Extraction failed. Try extracting manually to %GRADLE_HOME%
    pause
    exit /b 1
)

:setpath
set "PATH=%GRADLE_HOME%\gradle-8.5\bin;%PATH%"

:: Find Java
for %%d in ("F:\AI智能体\5\OpenJDK21*" "F:\AI软件相关\5\OpenJDK21*" "C:\Program Files\Eclipse Adoptium\*") do (
    if exist "%%d\bin\java.exe" (
        set "JDK_DIR=%%d"
        goto :javaok
    )
    for /d %%j in ("%%d\jdk-*") do (
        if exist "%%j\bin\java.exe" (
            set "JDK_DIR=%%j"
            goto :javaok
        )
    )
)
echo [ERROR] Java not found.
pause
exit /b 1

:javaok
echo Java: %JDK_DIR%
set "PATH=%JDK_DIR%\bin;%PATH%"

:: Build
cd /d "%~dp0"
echo.
echo ========================================
echo  Building Plugin...
echo ========================================

:: Generate wrapper
if not exist gradlew.bat (
    call gradle wrapper --gradle-version 7.6
)

:: Build
call gradlew.bat clean fatJar
if %ERRORLEVEL% NEQ 0 goto :fail

:: Copy to RuneLite
echo.
if not exist "%USERPROFILE%\.runelite\externalmanager" mkdir "%USERPROFILE%\.runelite\externalmanager"
copy /y build\libs\*-all.jar "%USERPROFILE%\.runelite\externalmanager\" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Plugin installed to RuneLite!
    echo Restart RuneLite ^> Settings ^> Plugins ^> search "OSRS Guru AI"
) else (
    echo JAR built but copy failed. Find it in: build\libs\
    dir build\libs\*.jar
)
goto :end

:fail
echo [ERROR] Build failed. Try running manually:
echo   cd %~dp0
echo   gradle fatJar

:end
pause
