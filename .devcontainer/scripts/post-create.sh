#!/bin/bash

# Optimized post-create script for Goldilocks development environment
set -e

echo "🚀 Starting optimized Goldilocks setup..."

# Configure Git safely
git config --global --add safe.directory "$(pwd)"

# Activate virtual environment (already created in Docker build)
export PATH="/opt/venv/bin:$PATH"

# Verify environment
echo "Python: $(python --version)"
echo "Pip: $(pip --version)"
echo "Flask: $(flask --version)"

# Set up pre-commit hooks if not already done
if [ ! -f ".git/hooks/pre-commit" ]; then
    pre-commit install --install-hooks
fi

# Ensure cache directories exist
mkdir -p "/home/app/.cache/pip" "/home/app/.npm"

echo "✅ Goldilocks development environment ready!"
echo "🔧 Run 'flask run --host 0.0.0.0 --port 9000' to start the development server"
