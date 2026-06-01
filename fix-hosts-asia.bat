@echo off
chcp 65001 >nul
REM ==========================================
REM OSRS Guide Site - GitHub Pages Hosts Fix (Asia CDN)
REM 使用亚洲 CDN 节点 (185.199.111.153)
REM ==========================================

echo.
echo ==========================================
echo   OSRS Guide Site - Hosts 修复工具 (亚洲节点)
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
set IP=185.199.111.153
set DOMAIN=ua202419891987.github.io
set ENTRY=%IP%    %DOMAIN%

echo [1/6] 备份 hosts 文件...
copy "%HOSTS_FILE%" "%BACKUP_FILE%" /Y >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [错误] 备份失败！
    pause
    exit /b 1
)
echo [√] 备份完成: %BACKUP_FILE%
echo.

echo [2/6] 移除旧的 github.io 配置...
findstr /V "ua202419891987.github.io" "%HOSTS_FILE%" > "%HOSTS_FILE%.tmp"
move /Y "%HOSTS_FILE%.tmp" "%HOSTS_FILE%" >nul 2>&1
echo [√] 旧配置已清除
echo.

echo [3/6] 添加新的 CDN 节点配置...
echo.>> "%HOSTS_FILE%"
echo # OSRS Guide Site - GitHub Pages Fix (Asia CDN, added %date% %time%)>> "%HOSTS_FILE%"
echo # 使用亚洲 CDN 节点 (185.199.111.153)>> "%HOSTS_FILE%"
echo %ENTRY%>> "%HOSTS_FILE%"
echo [√] 配置已添加: %ENTRY%
echo.

echo [4/6] 验证配置是否生效...
find /C "%ENTRY%" "%HOSTS_FILE%" >nul 2>&1
if %errorLevel% EQU 0 (
    echo [√] 验证通过！配置已生效
) else (
    echo [错误] 验证失败！请手动检查 hosts 文件
    pause
    exit /b 1
)
echo.

echo [5/6] 清除 DNS 缓存...
ipconfig /flushdns >nul 2>&1
if %errorLevel% EQU 0 (
    echo [√] DNS 缓存已清除
) else (
    echo [警告] DNS 缓存清除失败，请手动执行: ipconfig /flushdns
)
echo.

echo [6/6] 测试连接...
ping -n 2 %DOMAIN% >nul 2>&1
if %errorLevel% EQU 0 (
    echo [√] Ping 测试通过
) else (
    echo [警告] Ping 测试失败，但配置已生效
)
echo.

echo ==========================================
echo   配置完成！(使用亚洲 CDN 节点)
echo ==========================================
echo.
echo 下一步：
echo   1. 重启浏览器
echo   2. 访问: https://ua202419891987.github.io/osrs-guide-site/
echo.
echo 如果仍无法访问，请尝试：
echo   - 关闭 VPN/代理软件后重试
echo   - 使用手机热点测试
echo   - 等待 10 分钟后重试
echo.
echo 备用 CDN 节点 IP：
echo   185.199.108.153  (美国西海岸)
echo   185.199.109.153  (美国东海岸)
echo   185.199.110.153  (欧洲)
echo   185.199.111.153  (亚洲) [当前使用]
echo.
pause
