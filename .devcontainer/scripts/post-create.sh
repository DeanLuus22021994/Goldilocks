#!/bin/bash

# Optimized post-create script for Goldilocks development environment
set -e

echo "🚀 Starting optimized Goldilocks setup..."

# Set up workspace ownership (essential for volume mounts)
sudo chown -R vscode:vscode "$(pwd)"
mkdir -p "/home/vscode/.cache/pip" "/home/vscode/.npm"
sudo chown -R vscode:vscode "/home/vscode/.cache" "/home/vscode/.npm"

# Configure Git safely
git config --global --add safe.directory "$(pwd)"

# Create virtual environment if missing
if [ ! -f ".venv/bin/activate" ]; then
    python -m venv .venv --upgrade-deps
    sudo chown -R vscode:vscode .venv
fi

# Install Python dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install --install-hooks

# Set up Node.js environment if needed
if [ -f "package.json" ]; then
    npm ci
fi

echo "✅ Goldilocks setup complete!"
