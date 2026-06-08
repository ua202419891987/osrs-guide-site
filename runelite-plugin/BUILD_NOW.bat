@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo  OSRS Guru Plugin — Auto Build
echo ========================================
echo.

:: Find Java — scan common locations
set JAVA_EXE=
set JDK_DIR=

:: User's install path
for /d %%d in ("F:\AI*") do (
    for /d %%j in ("%%d\5\OpenJDK21*") do (
        if exist "%%j\jdk-21.0.11+10\bin\java.exe" (
            set "JDK_DIR=%%j\jdk-21.0.11+10"
            set "JAVA_EXE=%%j\jdk-21.0.11+10\bin\java.exe"
            goto :java_found
        )
        if exist "%%j\bin\java.exe" (
            set "JDK_DIR=%%j"
            set "JAVA_EXE=%%j\bin\java.exe"
            goto :java_found
        )
    )
)

:: Standard paths
for %%d in (
    "C:\Program Files\Eclipse Adoptium"
    "C:\Program Files\Java"
) do (
    for /r %%d %%j in (java.exe) do (
        if exist "%%j" (
            set "JAVA_EXE=%%j"
            for %%k in ("%%j\..\..") do set "JDK_DIR=%%~fk"
            goto :java_found
        )
    )
)

echo [ERROR] Java not found! Install JDK 21 from https://adoptium.net/
pause
exit /b 1

:java_found
echo [OK] Java found: %JAVA_EXE%
set "PATH=%JDK_DIR%\bin;%PATH%"
java -version 2>&1
echo.

:: Check Gradle
set GRADLE_CMD=
where gradle >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "GRADLE_CMD=gradle"
    echo [OK] Gradle found in PATH.
    goto :build
)

:: Install Gradle via winget
echo Gradle not found. Installing via winget...
winget install Gradle.Gradle --accept-package-agreements --accept-source-agreements -s winget 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Gradle installed. Please re-run this script.
    echo NOTE: You may need to close and reopen this terminal.
    pause
    exit /b 0
)

:: Fallback: download gradle
echo winget failed. Downloading Gradle directly...
set "GRADLE_ZIP=%TEMP%\gradle-8.5-bin.zip"
set "GRADLE_DIR=%USERPROFILE%\gradle"
curl -L --insecure -o "%GRADLE_ZIP%" "https://services.gradle.org/distributions/gradle-8.5-bin.zip" 2>&1
if exist "%GRADLE_ZIP%" (
    echo Extracting...
    powershell -Command "Expand-Archive -Path '%GRADLE_ZIP%' -DestinationPath '%GRADLE_DIR%' -Force" 2>&1
    set "GRADLE_CMD=%GRADLE_DIR%\gradle-8.5\bin\gradle.bat"
    set "PATH=%GRADLE_DIR%\gradle-8.5\bin;%PATH%"
    echo [OK] Gradle extracted to %GRADLE_DIR%
) else (
    echo [ERROR] Could not download Gradle. Please install manually: https://gradle.org/install/
    pause
    exit /b 1
)

:build
echo.
echo ========================================
echo  Building OSRS Guru Plugin...
echo ========================================
echo.

:: Generate wrapper
if not exist "gradlew.bat" (
    echo [1/3] Generating Gradle Wrapper...
    call "%GRADLE_CMD%" wrapper --gradle-version 7.6 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Wrapper generation failed.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Gradle Wrapper found.
)

:: Clean
echo [2/3] Cleaning...
call gradlew.bat clean 2>&1

:: Build fat JAR
echo [3/3] Building fat JAR...
call gradlew.bat fatJar 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed. Trying alternative: gradle jar
    call gradlew.bat jar 2>&1
)

:: Check result
if exist "build\libs\*.jar" (
    echo.
    echo ========================================
    echo  BUILD SUCCESSFUL!
    echo ========================================
    for %%f in (build\libs\*-all.jar) do (
        echo JAR: %%~dpnxf
        echo Size: %%~zf bytes
    )
    echo.
    echo Installing to RuneLite...
    if not exist "%USERPROFILE%\.runelite\externalmanager" mkdir "%USERPROFILE%\.runelite\externalmanager"
    copy /y build\libs\*-all.jar "%USERPROFILE%\.runelite\externalmanager\" 2>&1
    echo.
    echo DONE! Restart RuneLite and enable 'OSRS Guru AI' in Plugin settings.
) else (
    echo.
    echo [ERROR] JAR not found. Build may have failed silently.
    echo Check errors above or run: gradlew.bat fatJar --info
)

pause
