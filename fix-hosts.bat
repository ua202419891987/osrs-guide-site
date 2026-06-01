@echo off
chcp 65001 >nul
REM ==========================================
REM OSRS Guide Site - GitHub Pages Hosts Fix
REM 自动添加 github.io 域名到 hosts 文件
REM ==========================================

echo.
echo ==========================================
echo   OSRS Guide Site - Hosts 文件修复工具
echo ==========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [错误] 需要管理员权限！
    echo.
    echo 请右键此脚本，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo [√] 管理员权限确认
echo.

REM 设置变量
set HOSTS_FILE=%SystemRoot%\System32\drivers\etc\hosts
set BACKUP_FILE=%HOSTS_FILE%.backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set IP=185.199.108.153
set DOMAIN=ua202419891987.github.io
set ENTRY=%IP%    %DOMAIN%

echo [1/5] 备份 hosts 文件...
copy "%HOSTS_FILE%" "%BACKUP_FILE%" /Y >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [错误] 备份失败！
    pause
    exit /b 1
)
echo [√] 备份完成: %BACKUP_FILE%
echo.

echo [2/5] 检查是否已存在配置...
find /C "%DOMAIN%" "%HOSTS_FILE%" >nul 2>&1
if %errorLevel% EQU 0 (
    echo [!] 检测到已存在的配置，检查 IP 是否正确...
    find /C "%IP%    %DOMAIN%" "%HOSTS_FILE%" >nul 2>&1
    if %errorLevel% EQU 0 (
        echo [√] 配置已正确，无需修改
        goto :flush_dns
    ) else (
        echo [!] 发现旧配置，将更新...
        REM 删除旧配置
        findstr /V "%DOMAIN%" "%HOSTS_FILE%" > "%HOSTS_FILE%.tmp"
        move /Y "%HOSTS_FILE%.tmp" "%HOSTS_FILE%" >nul 2>&1
    )
)

echo.
echo [3/5] 添加新配置到 hosts 文件...
echo.>> "%HOSTS_FILE%"
echo # OSRS Guide Site - GitHub Pages Fix (added %date% %time%)>> "%HOSTS_FILE%"
echo %ENTRY%>> "%HOSTS_FILE%"
echo [√] 配置已添加: %ENTRY%
echo.

echo [4/5] 验证配置是否生效...
find /C "%ENTRY%" "%HOSTS_FILE%" >nul 2>&1
if %errorLevel% EQU 0 (
    echo [√] 验证通过！配置已生效
) else (
    echo [错误] 验证失败！请手动检查 hosts 文件
    pause
    exit /b 1
)
echo.

:flush_dns
echo [5/5] 清除 DNS 缓存...
ipconfig /flushdns >nul 2>&1
if %errorLevel% EQU 0 (
    echo [√] DNS 缓存已清除
) else (
    echo [警告] DNS 缓存清除失败，请手动执行: ipconfig /flushdns
)
echo.

echo ==========================================
echo   配置完成！
echo ==========================================
echo.
echo 下一步：
echo   1. 重启浏览器
echo   2. 访问: https://ua202419891987.github.io/osrs-guide-site/
echo.
echo 如果仍无法访问，请尝试：
echo   - 关闭 VPN/代理软件
echo   - 使用手机热点测试
echo   - 等待 10 分钟后重试
echo.
pause
