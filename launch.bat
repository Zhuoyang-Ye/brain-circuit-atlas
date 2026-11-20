@echo off
setlocal
title Brain Circuit Atlas v0.3

cd /d "%~dp0"

if exist "BrainCircuitAtlas.exe" (
    start "" "BrainCircuitAtlas.exe"
    exit /b 0
)

if exist "dist\BrainCircuitAtlas.exe" (
    start "" "dist\BrainCircuitAtlas.exe"
    exit /b 0
)

echo BrainCircuitAtlas.exe not found. Launching via Python server...
set PY=python
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 set PY=py

start "Brain Circuit Atlas Server" /min %PY% backend\server.py 8765
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8765/index.html
