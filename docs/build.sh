#!/bin/bash
# Documentation Build Script
# Downloads required tools to bin/ and builds documentation

set -e

DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="$DOCS_DIR/bin"

echo "🏗️  Building Goldilocks Documentation"
echo "======================================="

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Check if DocFX exists, download if not
if [ ! -f "$BIN_DIR/docfx" ] && [ ! -f "$BIN_DIR/docfx.exe" ]; then
    echo "📥 Downloading DocFX..."
    cd "$BIN_DIR"

    # Download appropriate version based on OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -q https://github.com/dotnet/docfx/releases/latest/download/docfx-linux-x64.zip
        unzip -q docfx-linux-x64.zip
        chmod +x docfx
        rm docfx-linux-x64.zip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        wget -q https://github.com/dotnet/docfx/releases/latest/download/docfx-osx-x64.zip
        unzip -q docfx-osx-x64.zip
        chmod +x docfx
        rm docfx-osx-x64.zip
    else
        echo "❌ Unsupported OS for automatic DocFX download"
        exit 1
    fi

    cd "$DOCS_DIR"
    echo "✅ DocFX downloaded successfully"
else
    echo "✅ DocFX already available"
fi

# Build documentation
echo "🔨 Building documentation..."
cd "$DOCS_DIR"

if [ -f "$BIN_DIR/docfx" ]; then
    "$BIN_DIR/docfx" docfx.json
elif [ -f "$BIN_DIR/docfx.exe" ]; then
    "$BIN_DIR/docfx.exe" docfx.json
else
    echo "❌ DocFX not found after download"
    exit 1
fi

echo "🎉 Documentation built successfully!"
echo "📖 Open _site/index.html to view the documentation"
