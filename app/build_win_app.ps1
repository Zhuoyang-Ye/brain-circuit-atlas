# app/build_win_app.ps1
# Builds Brain Circuit Atlas v0.3 for Windows into a native standalone executable.
[CmdletBinding()]
param(
    [switch]$ZipPackage
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path "$ScriptDir\.."
$DistDir = "$ProjectRoot\dist"

Write-Host "=== Building Brain Circuit Atlas v0.3 (Windows Native App) ===" -ForegroundColor Cyan

# 1. Ensure dist directory exists
if (!(Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir | Out-Null
}

# 2. Locate C# compiler
$CscCandidates = @(
    "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
    "C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
)

$CscPath = $null
foreach ($cand in $CscCandidates) {
    if (Test-Path $cand) {
        $CscPath = $cand
        break
    }
}

if (!$CscPath) {
    Write-Error "Microsoft .NET Framework C# compiler (csc.exe) not found."
}

Write-Host "Using C# compiler: $CscPath" -ForegroundColor DarkGray

# 3. Compile BrainCircuitAtlas.cs
$SourceFile = "$ScriptDir\BrainCircuitAtlas.cs"
$OutExe = "$DistDir\BrainCircuitAtlas.exe"

Write-Host "Compiling $SourceFile -> $OutExe..." -ForegroundColor Yellow

& $CscPath /nologo /optimize+ /target:winexe /out:"$OutExe" `
    /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll `
    "$SourceFile"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Compilation failed with exit code $LASTEXITCODE."
}

Write-Host "Successfully compiled: $OutExe" -ForegroundColor Green

# Also copy to root for instant double-click convenience
Copy-Item "$OutExe" "$ProjectRoot\BrainCircuitAtlas.exe" -Force
Write-Host "Copied executable to project root: $ProjectRoot\BrainCircuitAtlas.exe" -ForegroundColor Green

# 4. Optional packaging into release zip
if ($ZipPackage) {
    $ZipPath = "$DistDir\Brain-Circuit-Atlas-v0.3.0-Windows.zip"
    Write-Host "Packaging release zip: $ZipPath..." -ForegroundColor Yellow

    $PackageDir = "$DistDir\package_temp"
    if (Test-Path $PackageDir) { Remove-Item $PackageDir -Recurse -Force }
    New-Item -ItemType Directory -Path "$PackageDir\BrainCircuitAtlas" | Out-Null

    Copy-Item "$OutExe" "$PackageDir\BrainCircuitAtlas\"
    Copy-Item "$ProjectRoot\index.html" "$PackageDir\BrainCircuitAtlas\"
    Copy-Item "$ProjectRoot\backend" "$PackageDir\BrainCircuitAtlas\" -Recurse
    Copy-Item "$ProjectRoot\data" "$PackageDir\BrainCircuitAtlas\" -Recurse
    Copy-Item "$ProjectRoot\js" "$PackageDir\BrainCircuitAtlas\" -Recurse
    Copy-Item "$ProjectRoot\css" "$PackageDir\BrainCircuitAtlas\" -Recurse
    if (Test-Path "$ProjectRoot\launch.bat") { Copy-Item "$ProjectRoot\launch.bat" "$PackageDir\BrainCircuitAtlas\" }

    if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
    Compress-Archive -Path "$PackageDir\BrainCircuitAtlas" -DestinationPath "$ZipPath"
    Remove-Item $PackageDir -Recurse -Force
    Write-Host "Created release archive: $ZipPath" -ForegroundColor Green
}

Write-Host "=== Windows Build Complete! ===" -ForegroundColor Cyan
