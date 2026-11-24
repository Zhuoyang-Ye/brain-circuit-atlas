@echo off
setlocal
echo ===================================================
echo  Building Brain Circuit Atlas v0.3 for Windows
echo ===================================================

set CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe
if not exist "%CSC%" set CSC=C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe

if not exist "%CSC%" (
    echo Error: csc.exe compiler not found in Microsoft.NET Framework.
    pause
    exit /b 1
)

if not exist "..\dist" mkdir "..\dist"

echo Compiling BrainCircuitAtlas.cs with embedded icon...
if exist "%~dp0AppIcon.ico" (
    "%CSC%" /nologo /optimize+ /target:winexe /win32icon:"%~dp0AppIcon.ico" /out:"..\dist\BrainCircuitAtlas.exe" /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll "%~dp0BrainCircuitAtlas.cs"
) else (
    "%CSC%" /nologo /optimize+ /target:winexe /out:"..\dist\BrainCircuitAtlas.exe" /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll "%~dp0BrainCircuitAtlas.cs"
)

if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed with code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

copy /y "..\dist\BrainCircuitAtlas.exe" "..\BrainCircuitAtlas.exe" >nul
echo Built successfully: dist\BrainCircuitAtlas.exe and BrainCircuitAtlas.exe
pause
