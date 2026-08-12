@echo off
chcp 65001 >nul
cd /d "%~dp0"
start /min "" python -m http.server 8765
