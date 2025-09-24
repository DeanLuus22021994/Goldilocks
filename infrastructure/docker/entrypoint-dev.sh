#!/bin/bash
# Development entrypoint script with performance optimizations

set -e

echo "🚀 Starting Goldilocks development server with optimizations..."

# Activate virtual environment
source /opt/venv/bin/activate

# Set development environment variables
export FLASK_APP=goldilocks.app
export FLASK_ENV=development
export FLASK_DEBUG=1

# Add current directory to Python path for development
export PYTHONPATH="/app/src:${PYTHONPATH}"

# Performance optimizations for development
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=0
export FLASK_SKIP_DOTENV=1

# Create cache directories with proper permissions
mkdir -p /tmp/goldilocks-cache/{pip,mypy,pytest,ruff,pre-commit}
chown -R app:app /tmp/goldilocks-cache 2>/dev/null || true

# Run database migrations if they exist
if [ -f "/app/migrations/env.py" ]; then
    echo "Running database migrations..."
    python -m flask db upgrade || echo "No migrations to run"
fi

# Fix any permission issues
if [ -d "/workspaces/Goldilocks/.git" ]; then
    echo "Ensuring proper git permissions..."
    sudo chown -R app:app /workspaces/Goldilocks/.git/ 2>/dev/null || true
    sudo chmod -R u+w /workspaces/Goldilocks/.git/ 2>/dev/null || true
fi

# Start Flask development server with hot reload
echo "🔥 Starting Flask with hot reload..."
exec python -m flask run --host=0.0.0.0 --port=9000 --reload --debugger --with-threads
