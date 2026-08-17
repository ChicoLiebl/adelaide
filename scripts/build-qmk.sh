#!/bin/sh
# Builds the QMK firmware for both keyboards in this repo.
# The QMK build system lives in the qmk_firmware repo; this script clones it
# (shallow) on first run and symlinks this repo's keyboard definitions into it.
set -e

BASE_DIR=$(git rev-parse --show-toplevel)
QMK_HOME="${QMK_HOME:-$HOME/qmk_firmware}"
KEYBOARDS="adelaide my_numpad"

if ! command -v qmk >/dev/null 2>&1; then
    echo "❌ qmk CLI not found. Install it first (e.g. pacman -S qmk / pip install qmk)" >&2
    exit 1
fi
if ! command -v avr-gcc >/dev/null 2>&1; then
    echo "❌ avr-gcc not found. Install the AVR toolchain (e.g. pacman -S avr-gcc avr-libc)" >&2
    exit 1
fi

# --- Get qmk_firmware on first run ---
if [ ! -d "$QMK_HOME/keyboards" ]; then
    echo "Cloning qmk_firmware into $QMK_HOME (first run only)..."
    git clone --depth 1 https://github.com/qmk/qmk_firmware.git "$QMK_HOME"
    git -C "$QMK_HOME" submodule update --init --recursive --depth 1
fi
qmk config user.qmk_home="$QMK_HOME" >/dev/null

# --- Link this repo's keyboards into the QMK tree ---
for KB in $KEYBOARDS; do
    ln -sfn "$BASE_DIR/qmk/$KB" "$QMK_HOME/keyboards/$KB"
done

# --- Build ---
GIT_VERSION=$(git describe --abbrev=6 --dirty --always --tags --long)
OUT_DIR="$BASE_DIR/FAB-OUTPUTS/firmware-$(date +%y-%m-%d)-$GIT_VERSION"
mkdir -p "$OUT_DIR"

for KB in $KEYBOARDS; do
    echo "=== Building $KB ==="
    qmk compile -kb "$KB" -km default
    cp "$QMK_HOME/${KB}_default.hex" "$OUT_DIR/"
done

echo "✅ Firmware binaries in $OUT_DIR:"
ls "$OUT_DIR"
