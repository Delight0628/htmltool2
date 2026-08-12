@echo off
chcp 65001 >nul
echo ========================================
echo   页琢 - 打包脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 检查依赖...
pip install pystray Pillow pyinstaller -q

echo [2/2] 开始打包...
python -m PyInstaller build.spec --clean --noconfirm

if exist "dist\页琢.exe" (
    echo.
    echo ========================================
    echo   打包成功！
    echo   产物: dist\页琢.exe
    echo ========================================
) else (
    echo.
    echo   打包失败，请检查上方日志
)
pause
