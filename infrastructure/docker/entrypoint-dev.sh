#!/bin/bash
# Development entrypoint script

set -e

echo "🚀 Starting Goldilocks development server..."

# Activate virtual environment
source /opt/venv/bin/activate

# Set development environment variables
export FLASK_APP=goldilocks.app
export FLASK_ENV=development
export FLASK_DEBUG=1

# Add current directory to Python path for development
export PYTHONPATH="/app/src:${PYTHONPATH}"

# Run database migrations if they exist
if [ -f "/app/migrations/env.py" ]; then
    echo "Running database migrations..."
    python -m flask db upgrade || echo "No migrations to run"
fi

# Start Flask development server with hot reload
exec python -m flask run --host=0.0.0.0 --port=9000 --reload --debugger
