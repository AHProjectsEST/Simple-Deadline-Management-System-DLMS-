#!/usr/bin/env bash

# Optional scaling settings
export GDK_SCALE=2
export GDK_DPI_SCALE=0.5

# Resolve the directory where this script lives
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Run the Python script and log output inside the app directory
python3 "$SCRIPT_DIR/DLMS.py" >> "$SCRIPT_DIR/DLMS_startup.log" 2>&1

