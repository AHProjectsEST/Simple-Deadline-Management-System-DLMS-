#!/usr/bin/env bash

APP_DIR="$HOME/.local/share/DLMS"
DESKTOP_DIR="$HOME/.local/share/applications"

# Create app directory
mkdir -p "$APP_DIR"

# Copy program files
cp DLMS.py run.sh icon.png "$APP_DIR"

# Make launcher executable
chmod +x "$APP_DIR/run.sh"

# Generate desktop file with correct paths
sed \
    -e "s|{APP_DIR}|$APP_DIR|g" \
    -e "s|{ICON_PATH}|$APP_DIR/icon.png|g" \
    DLMS.desktop > "$DESKTOP_DIR/DLMS.desktop"

chmod +x "$DESKTOP_DIR/DLMS.desktop"

echo "Installed! You can now launch DLMS from your applications menu."
