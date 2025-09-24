#!/bin/bash
# Post-create script for devcontainer - optimized for instant setup

set -e

echo "🚀 Setting up Goldilocks development environment..."

# Ensure we're in the right directory
cd /workspaces/Goldilocks || exit 1

# Configure Git safely
git config --global --add safe.directory "$(pwd)"

# Activate virtual environment
export PATH="/opt/venv/bin:$PATH"

# Verify environment
echo "✅ Environment check:"
echo "  Python: $(python --version)"
echo "  Pip: $(pip --version)"
echo "  Flask: $(flask --version)"

# Setup pre-commit hooks if git repo exists
if [ -d ".git" ]; then
    echo "🔧 Setting up pre-commit hooks..."
    pre-commit install --install-hooks || echo "Pre-commit setup skipped"
fi

# Ensure cache directories exist with proper permissions
sudo mkdir -p /tmp/goldilocks-cache/{pip,npm,pre-commit,mypy,pytest,ruff}
sudo chown -R app:app /tmp/goldilocks-cache

echo ""
echo "✅ Development environment ready!"
echo "🔥 Run 'flask run --host 0.0.0.0 --port 9000' to start development server"
echo "🧪 Run 'pytest' to run tests"
echo "🎨 Run 'pre-commit run --all-files' to format code"
