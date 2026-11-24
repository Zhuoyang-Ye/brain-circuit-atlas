#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

DIST_DIR="$DIR/dist"
mkdir -p "$DIST_DIR"
STAGE_DIR="/tmp/BrainCircuitAtlas_Win_$$"
rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR/BrainCircuitAtlas"

echo "=== Staging Windows release package ==="
cp "$DIR/index.html" "$STAGE_DIR/BrainCircuitAtlas/"
cp "$DIR/launch.bat" "$STAGE_DIR/BrainCircuitAtlas/"
cp "$DIR/BrainCircuitAtlas.vbs" "$STAGE_DIR/BrainCircuitAtlas/"

# Copy directories
cp -R "$DIR/css" "$STAGE_DIR/BrainCircuitAtlas/"
cp -R "$DIR/js" "$STAGE_DIR/BrainCircuitAtlas/"
cp -R "$DIR/data" "$STAGE_DIR/BrainCircuitAtlas/"
cp -R "$DIR/backend" "$STAGE_DIR/BrainCircuitAtlas/"
cp -R "$DIR/tools" "$STAGE_DIR/BrainCircuitAtlas/"
mkdir -p "$STAGE_DIR/BrainCircuitAtlas/app"
cp "$DIR/app/BrainCircuitAtlas.cs" "$STAGE_DIR/BrainCircuitAtlas/app/"
cp "$DIR/app/build_win_app.bat" "$STAGE_DIR/BrainCircuitAtlas/app/"
cp "$DIR/app/build_win_app.ps1" "$STAGE_DIR/BrainCircuitAtlas/app/"
cp "$DIR/app/AppIcon.ico" "$STAGE_DIR/BrainCircuitAtlas/app/"

# Create README_WINDOWS.txt
cat << 'EOF' > "$STAGE_DIR/BrainCircuitAtlas/README_WINDOWS.txt"
========================================================================
 Brain Circuit Atlas v0.3 - Windows Desktop Distribution
========================================================================

SYSTEM REQUIREMENTS:
• Windows 10 or Windows 11
• Python 3.8+ (from https://www.python.org/ or the Microsoft Store)
• Microsoft Edge or Google Chrome (for hardware-accelerated 3D WebGL)

HOW TO RUN:
1. Double-click "launch.bat" (or "BrainCircuitAtlas.vbs" for silent launch).
   - This starts the local Python backend server and opens the 3D Atlas in a sleek standalone desktop window.
2. (Optional) Compile a native standalone BrainCircuitAtlas.exe:
   - Double-click "app\build_win_app.bat"
   - It compiles BrainCircuitAtlas.cs using the built-in Microsoft C# compiler (csc.exe) and embeds the official app icon.

WINDOWS DISPLAY & NAVIGATION SHORTCUTS:

Display & Zoom:
• Zoom In:                      Ctrl + +  or  Ctrl + =
• Zoom Out:                     Ctrl + -
• Actual Size (100%):           Ctrl + 0
• Full Screen:                  F11  or  Ctrl + Shift + F
• Toggle Dark / Light Theme:    Ctrl + Shift + D
• Toggle 3D Labels:             Ctrl + Shift + L
• Toggle Brain Surface (3D):    Ctrl + Shift + B
• Toggle Signal Flow (3D):      Ctrl + Shift + A
• Reset 3D Camera / Overview:   Ctrl + Alt + 0

Atlas Views:
• 3D Atlas:                     Ctrl + 1
• Functional Map:               Ctrl + 2
• Microcircuit:                 Ctrl + 3
• Cells & Molecules:            Ctrl + 4
• Across Scales:                Ctrl + 5
• Evidence & Gaps:              Ctrl + 6
• Hypothesis Lab:               Ctrl + 7
• Literature Library:           Ctrl + 8
• History Back / Forward:       Alt + Left / Alt + Right

Search & Panels:
• Search / Find in Atlas:       Ctrl + F  or  /
• Close Details Panel / Esc:    Esc
• Reload Page:                  Ctrl + R  or  F5
• Force Reload:                 Ctrl + Shift + R  or  Ctrl + F5
========================================================================
EOF

ZIP_OUT="$DIST_DIR/Brain-Circuit-Atlas-Windows.zip"
rm -f "$ZIP_OUT"

echo "Creating Windows zip archive: $ZIP_OUT"
cd "$STAGE_DIR"
zip -r -q "$ZIP_OUT" BrainCircuitAtlas
rm -rf "$STAGE_DIR"

echo "Windows release package ready: $ZIP_OUT"
ls -lh "$ZIP_OUT"
