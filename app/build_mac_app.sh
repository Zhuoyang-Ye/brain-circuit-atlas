#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

DIST_DIR="$DIR/dist"
APP_NAME="Brain Circuit Atlas"
APP_BUNDLE="$DIST_DIR/$APP_NAME.app"
DMG_PATH="$DIST_DIR/$APP_NAME.dmg"
ZIP_PATH="$DIST_DIR/Brain-Circuit-Atlas-macOS.zip"

echo "=== Building Brain Circuit Atlas for macOS ==="

rm -rf "$APP_BUNDLE" "$DMG_PATH" "$ZIP_PATH"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"
mkdir -p "/tmp/clang-cache"

echo "1. Generating application icon..."
if [ ! -f "app/AppIcon.icns" ]; then
    swift -module-cache-path /tmp/clang-cache app/make_icon.swift
    iconutil -c icns /tmp/AppIcon.iconset -o app/AppIcon.icns
    rm -rf /tmp/AppIcon.iconset
fi
cp "app/AppIcon.icns" "$APP_BUNDLE/Contents/Resources/AppIcon.icns"

echo "2. Compiling native macOS executable (Swift / ARM64)..."
swiftc -O -module-cache-path /tmp/clang-cache app/main.swift -o "$APP_BUNDLE/Contents/MacOS/BrainCircuitAtlas"
chmod +x "$APP_BUNDLE/Contents/MacOS/BrainCircuitAtlas"

echo "3. Copying Info.plist and metadata..."
cp "app/Info.plist" "$APP_BUNDLE/Contents/Info.plist"

echo "4. Bundling Python backend & web application assets..."
mkdir -p "$APP_BUNDLE/Contents/Resources/backend"
cp backend/*.py "$APP_BUNDLE/Contents/Resources/backend/"

# Copy web files
cp index.html "$APP_BUNDLE/Contents/Resources/"
cp -R css "$APP_BUNDLE/Contents/Resources/"
cp -R js "$APP_BUNDLE/Contents/Resources/"
cp -R data "$APP_BUNDLE/Contents/Resources/"
cp -R tools "$APP_BUNDLE/Contents/Resources/"

echo "5. Creating downloadable macOS Zip archive..."
ditto -c -k --keepParent "$APP_BUNDLE" "$ZIP_PATH"

echo "6. Creating mountable macOS DMG installer (optional)..."
DMG_STAGE="/tmp/bca_dmg_stage_$$"
rm -rf "$DMG_STAGE"
mkdir -p "$DMG_STAGE"
cp -R "$APP_BUNDLE" "$DMG_STAGE/"
if diskutil image create from "$DMG_STAGE" "$DMG_PATH" --format UDZO --volumeName "$APP_NAME" >/dev/null 2>&1 || \
   hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_STAGE" -ov -format UDZO "$DMG_PATH" >/dev/null 2>&1; then
    echo "DMG created at $DMG_PATH"
else
    echo "Note: DMG disk mount creation restricted by current shell sandbox; Zip archive ready at $ZIP_PATH."
fi
rm -rf "$DMG_STAGE"

echo ""
echo "=== Build Complete! ==="
echo "Application bundle: $APP_BUNDLE"
echo "Downloadable Zip:   $ZIP_PATH"
if [ -f "$DMG_PATH" ]; then
    echo "Downloadable DMG:   $DMG_PATH"
fi
ls -lh "$DIST_DIR"
