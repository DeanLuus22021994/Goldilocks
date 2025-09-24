#!/bin/bash
# Production entrypoint script with performance optimizations

set -e

echo "🚀 Starting Goldilocks production server with optimizations..."

# Activate virtual environment
source /opt/venv/bin/activate

# Set production environment variables
export FLASK_APP=goldilocks.app
export FLASK_ENV=production
export FLASK_DEBUG=0

# Add app directory to Python path for bytecode imports
export PYTHONPATH="/app:${PYTHONPATH}"

# Production performance optimizations
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=2
export FLASK_SKIP_DOTENV=1

# Gunicorn configuration with performance tuning
WORKERS="${WORKERS:-$(nproc)}"
WORKER_CLASS="${WORKER_CLASS:-sync}"
WORKER_CONNECTIONS="${WORKER_CONNECTIONS:-1000}"
MAX_REQUESTS="${MAX_REQUESTS:-1000}"
MAX_REQUESTS_JITTER="${MAX_REQUESTS_JITTER:-100}"
TIMEOUT="${TIMEOUT:-30}"
KEEPALIVE="${KEEPALIVE:-5}"
PRELOAD="${PRELOAD:-true}"

# Run database migrations if they exist
if [ -f "/app/migrations/env.py" ]; then
    echo "Running database migrations..."
    python -m flask db upgrade || echo "No migrations to run"
fi

# Health check before starting
echo "🏥 Running health check..."
python -c "
import sys
sys.path.insert(0, '/app')
try:
    from goldilocks.app import app
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
    print('✅ Application health check passed')
except Exception as e:
    print(f'❌ Health check failed: {e}')
    sys.exit(1)
"

echo "⚡ Starting production server with ${WORKERS} workers..."
# Start production server with gunicorn
exec python -m gunicorn \
    --bind 0.0.0.0:9000 \
    --workers "$WORKERS" \
    --worker-class "$WORKER_CLASS" \
    --worker-connections "$WORKER_CONNECTIONS" \
    --timeout "$TIMEOUT" \
    --keep-alive "$KEEPALIVE" \
    --max-requests "$MAX_REQUESTS" \
    --max-requests-jitter "$MAX_REQUESTS_JITTER" \
    --preload-app="$PRELOAD" \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    goldilocks.app:app
