@echo off
chcp 65001 >nul 2>&1
title VirtualMouse Server

if exist "%~dp0VirtualMouseServer.exe" (
    "%~dp0VirtualMouseServer.exe"
    pause
    exit /b 0
)

if exist "%~dp0dist\VirtualMouseServer.exe" (
    "%~dp0dist\VirtualMouseServer.exe"
    pause
    exit /b 0
)

echo [提示] 未找到打包的exe，尝试用Python启动...
echo.
echo [1/2] 检查并安装依赖...
pip install -r "%~dp0requirements.txt" --quiet
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败，请检查 Python 和 pip 是否已安装。
    echo 下载 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [2/2] 启动服务器...
echo.
python "%~dp0virtual_mouse_server.py"

pause
