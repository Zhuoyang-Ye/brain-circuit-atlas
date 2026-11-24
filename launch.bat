@echo off
setlocal enabledelayedexpansion
title Brain Circuit Atlas

echo ===================================================
echo   Brain Circuit Atlas (Windows Host)
echo ===================================================

:: 1. Check for compiled standalone executable
if exist "dist\BrainCircuitAtlas.exe" (
    start "" "dist\BrainCircuitAtlas.exe"
    exit /b 0
)
if exist "BrainCircuitAtlas.exe" (
    start "" "BrainCircuitAtlas.exe"
    exit /b 0
)

:: 2. If not yet compiled, attempt to build BrainCircuitAtlas.exe automatically via csc.exe
set "CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "!CSC!" set "CSC=C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"

if exist "!CSC!" (
    echo Compiling native executable BrainCircuitAtlas.exe...
    if not exist "dist" mkdir "dist"
    if exist "app\AppIcon.ico" (
        "!CSC!" /nologo /optimize+ /target:winexe /win32icon:"app\AppIcon.ico" /out:"dist\BrainCircuitAtlas.exe" /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll "app\BrainCircuitAtlas.cs" >nul 2>&1
    ) else (
        "!CSC!" /nologo /optimize+ /target:winexe /out:"dist\BrainCircuitAtlas.exe" /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll "app\BrainCircuitAtlas.cs" >nul 2>&1
    )
    if exist "dist\BrainCircuitAtlas.exe" (
        copy /y "dist\BrainCircuitAtlas.exe" "BrainCircuitAtlas.exe" >nul 2>&1
        start "" "BrainCircuitAtlas.exe"
        exit /b 0
    )
)

:: 3. Direct Python launch fallback
set "PYEXE="
where python >nul 2>&1 && set "PYEXE=python"
if not defined PYEXE where py >nul 2>&1 && set "PYEXE=py"
if not defined PYEXE (
    if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    if exist "%ProgramFiles%\Python313\python.exe" set "PYEXE=%ProgramFiles%\Python313\python.exe"
    if exist "%ProgramFiles%\Python312\python.exe" set "PYEXE=%ProgramFiles%\Python312\python.exe"
    if exist "%ProgramFiles%\Python311\python.exe" set "PYEXE=%ProgramFiles%\Python311\python.exe"
)

if not defined PYEXE (
    echo.
    echo [ERROR] Python 3.8+ was not found on your system.
    echo Please install Python from https://www.python.org/ or Microsoft Store and ensure it is added to PATH.
    echo.
    pause
    exit /b 1
)

echo Starting Brain Circuit Atlas backend server on http://127.0.0.1:8765 ...
start "" /b "%PYEXE%" backend\server.py 8765

:: Wait briefly for server startup
timeout /t 2 /nobreak >nul

:: Launch Edge in app mode if available
set "EDGE_EXE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE_EXE%" set "EDGE_EXE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE_EXE%" set "EDGE_EXE=%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"

if exist "%EDGE_EXE%" (
    start "" "%EDGE_EXE%" --app="http://127.0.0.1:8765/index.html" --window-size=1400,900
    exit /b 0
)

:: Launch Chrome in app mode if available
set "CHROME_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_EXE%" set "CHROME_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_EXE%" set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if exist "%CHROME_EXE%" (
    start "" "%CHROME_EXE%" --app="http://127.0.0.1:8765/index.html" --window-size=1400,900
    exit /b 0
)

:: Fallback to default browser
start "" "http://127.0.0.1:8765/index.html"
