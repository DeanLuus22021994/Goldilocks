#!/bin/bash
# Production entrypoint script

set -e

echo "🚀 Starting Goldilocks production server..."

# Activate virtual environment
source /opt/venv/bin/activate

# Set production environment variables
export FLASK_APP=goldilocks.app
export FLASK_ENV=production
export FLASK_DEBUG=0

# Add app directory to Python path for bytecode imports
export PYTHONPATH="/app:${PYTHONPATH}"

# Run database migrations if they exist
if [ -f "/app/migrations/env.py" ]; then
    echo "Running database migrations..."
    python -m flask db upgrade || echo "No migrations to run"
fi

# Start production server with gunicorn
exec python -m gunicorn \
    --bind 0.0.0.0:9000 \
    --workers "${WORKERS:-2}" \
    --timeout "${TIMEOUT:-30}" \
    --keep-alive "${KEEP_ALIVE:-2}" \
    --max-requests "${MAX_REQUESTS:-1000}" \
    --max-requests-jitter "${MAX_REQUESTS_JITTER:-100}" \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    goldilocks.app:app
