# Brain Circuit Atlas v0.3 - PowerShell Launcher
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

if (Test-Path "$ScriptDir\BrainCircuitAtlas.exe") {
    Start-Process "$ScriptDir\BrainCircuitAtlas.exe"
    exit 0
}

if (Test-Path "$ScriptDir\dist\BrainCircuitAtlas.exe") {
    Start-Process "$ScriptDir\dist\BrainCircuitAtlas.exe"
    exit 0
}

Write-Host "Launching Brain Circuit Atlas server..." -ForegroundColor Cyan
Start-Process "python" -ArgumentList "backend\server.py 8765" -WindowStyle Hidden
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:8765/index.html"
