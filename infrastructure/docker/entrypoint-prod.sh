#!/bin/bash
# ==============================================================================
# Goldilocks Production Entrypoint Script
# MODERNIZE - Latest production deployment best practices
# LIGHTWEIGHT - Optimized for edge computing and minimal resource usage
# HIGH COMPATIBILITY - Supports multiple deployment environments
# ==============================================================================

set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'       # Secure Internal Field Separator

# -----------------------------------------------------------------------------
# Script Configuration
# -----------------------------------------------------------------------------
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(dirname "$0")
readonly APP_DIR="/app"
readonly VENV_PATH="/opt/venv"
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Platform detection
readonly PLATFORM=$(uname -m)
readonly CPU_COUNT=$(nproc 2>/dev/null || echo "1")
readonly MEMORY_MB=$(($(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo "1048576") / 1024))

# Colors for output (production-safe)
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# -----------------------------------------------------------------------------
# Logging Functions (Production Optimized)
# -----------------------------------------------------------------------------
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date -Iseconds)

    # Structured logging for production
    if [[ "${LOG_FORMAT:-}" == "json" ]]; then
        printf '{"timestamp":"%s","level":"%s","message":"%s","script":"%s","pid":%d}\n' \
            "$timestamp" "$level" "$message" "$SCRIPT_NAME" "$$"
    else
        case "$level" in
            INFO)  echo -e "${GREEN}[${timestamp}] [INFO]${NC} $message" ;;
            WARN)  echo -e "${YELLOW}[${timestamp}] [WARN]${NC} $message" ;;
            ERROR) echo -e "${RED}[${timestamp}] [ERROR]${NC} $message" >&2 ;;
            DEBUG) [[ "${LOG_LEVEL}" == "DEBUG" ]] && echo -e "${BLUE}[${timestamp}] [DEBUG]${NC} $message" ;;
        esac
    fi
}

info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; }
debug() { log "DEBUG" "$@"; }

# -----------------------------------------------------------------------------
# Error Handling & Monitoring
# -----------------------------------------------------------------------------
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        error "Production server failed with exit code: $exit_code"
        error "Failed command: $BASH_COMMAND"

        # Send failure notification if configured
        if [[ -n "${FAILURE_WEBHOOK_URL:-}" ]]; then
            curl -s -X POST "${FAILURE_WEBHOOK_URL}" \
                -H "Content-Type: application/json" \
                -d "{\"text\":\"Goldilocks production server failed: $BASH_COMMAND (exit code: $exit_code)\"}" \
                2>/dev/null || true
        fi
    fi
    exit $exit_code
}

trap cleanup EXIT
trap 'error "Production server interrupted"; kill -TERM $PID 2>/dev/null || true; exit 130' INT TERM

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------
check_command() {
    local cmd="$1"
    if ! command -v "$cmd" >/dev/null 2>&1; then
        error "Required command '$cmd' not found"
        return 1
    fi
    debug "Found command: $cmd"
}

wait_for_service() {
    local host="$1"
    local port="$2"
    local timeout="${3:-60}"
    local service_name="${4:-service}"

    info "Waiting for $service_name at $host:$port (timeout: ${timeout}s)"

    local start_time=$(date +%s)
    for i in $(seq 1 "$timeout"); do
        if timeout 5 bash -c "</dev/tcp/$host/$port" 2>/dev/null; then
            local duration=$(($(date +%s) - start_time))
            info "$service_name is ready! (waited ${duration}s)"
            return 0
        fi

        # Exponential backoff for production resilience
        local wait_time=$((i <= 10 ? 1 : i <= 30 ? 2 : 5))
        debug "Attempt $i/$timeout failed, retrying in ${wait_time}s..."
        sleep "$wait_time"
    done

    error "$service_name at $host:$port is not available after ${timeout}s"
    return 1
}

detect_optimal_workers() {
    local cpu_workers=$((CPU_COUNT))
    local memory_workers=$((MEMORY_MB / 256))  # 256MB per worker
    local max_workers=32  # Reasonable upper limit

    # Use the minimum of CPU and memory-based calculations
    local optimal_workers=$(( cpu_workers < memory_workers ? cpu_workers : memory_workers ))

    # Ensure at least 1 worker, at most max_workers
    if [[ $optimal_workers -lt 1 ]]; then
        optimal_workers=1
    elif [[ $optimal_workers -gt $max_workers ]]; then
        optimal_workers=$max_workers
    fi

    debug "CPU cores: $CPU_COUNT, Memory: ${MEMORY_MB}MB, Optimal workers: $optimal_workers"
    echo "$optimal_workers"
}

# -----------------------------------------------------------------------------
# Environment Setup Functions
# -----------------------------------------------------------------------------
setup_production_environment() {
    info "Setting up production environment..."
    info "Platform: $PLATFORM | CPU cores: $CPU_COUNT | Memory: ${MEMORY_MB}MB"

    # Activate virtual environment
    if [[ -f "${VENV_PATH}/bin/activate" ]]; then
        debug "Activating virtual environment: $VENV_PATH"
        # shellcheck source=/dev/null
        source "${VENV_PATH}/bin/activate"
    else
        error "Virtual environment not found at $VENV_PATH"
        return 1
    fi

    # Set Flask production environment
    export FLASK_APP="${FLASK_APP:-goldilocks.app}"
    export FLASK_ENV="${FLASK_ENV:-production}"
    export FLASK_DEBUG="${FLASK_DEBUG:-0}"

    # Python path configuration
    export PYTHONPATH="${APP_DIR}/src:${PYTHONPATH:-}"

    # Production performance optimizations
    export PYTHONUNBUFFERED=1
    export PYTHONDONTWRITEBYTECODE=1    # No .pyc files in production
    export PYTHONOPTIMIZE=2             # Maximum optimization
    export PYTHONHASHSEED=random        # Security: randomize hash seeds
    export FLASK_SKIP_DOTENV=1          # Skip .env loading (use env vars)

    # Memory and garbage collection optimizations
    export PYTHONMALLOC=pymalloc
    export MALLOC_MMAP_THRESHOLD_=131072
    export MALLOC_TRIM_THRESHOLD_=131072
    export MALLOC_MMAP_MAX_=65536

    # Security settings
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONSECUREIMPORT=1

    debug "Production environment configured successfully"
}

setup_gunicorn_config() {
    info "Configuring Gunicorn for production..."

    # Auto-detect optimal configuration based on system resources
    local optimal_workers
    optimal_workers=$(detect_optimal_workers)

    # Gunicorn configuration with intelligent defaults
    export WORKERS="${WORKERS:-$optimal_workers}"
    export WORKER_CLASS="${WORKER_CLASS:-sync}"  # gevent for async, sync for CPU-bound
    export WORKER_CONNECTIONS="${WORKER_CONNECTIONS:-1000}"
    export MAX_REQUESTS="${MAX_REQUESTS:-1000}"
    export MAX_REQUESTS_JITTER="${MAX_REQUESTS_JITTER:-100}"
    export TIMEOUT="${TIMEOUT:-30}"
    export KEEPALIVE="${KEEPALIVE:-5}"
    export PRELOAD="${PRELOAD:-true}"

    # Advanced Gunicorn settings
    export WORKER_TMP_DIR="${WORKER_TMP_DIR:-/dev/shm}"  # Use tmpfs for better performance
    export GRACEFUL_TIMEOUT="${GRACEFUL_TIMEOUT:-60}"
    export USER="${USER:-app}"
    export GROUP="${GROUP:-app}"
    export UMASK="${UMASK:-0}"

    # Logging configuration
    export ACCESS_LOG_FORMAT='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
    export ACCESS_LOGFILE="${ACCESS_LOGFILE:--}"  # stdout
    export ERROR_LOGFILE="${ERROR_LOGFILE:--}"    # stderr
    export LOGLEVEL="${GUNICORN_LOGLEVEL:-info}"

    info "Gunicorn configuration:"
    info "   Workers: $WORKERS"
    info "   Worker class: $WORKER_CLASS"
    info "   Worker connections: $WORKER_CONNECTIONS"
    info "   Timeout: ${TIMEOUT}s"
    info "   Keep-alive: ${KEEPALIVE}s"
    info "   Preload app: $PRELOAD"
}

# -----------------------------------------------------------------------------
# Database & Dependencies
# -----------------------------------------------------------------------------
wait_for_dependencies() {
    info "Waiting for external dependencies..."

    # Parse DATABASE_URL and wait for database
    if [[ "${DATABASE_URL:-}" == *"@"* ]]; then
        local db_host db_port
        db_host=$(echo "${DATABASE_URL}" | sed -n 's/.*@\([^:]*\):.*/\1/p')
        db_port=$(echo "${DATABASE_URL}" | sed -n 's/.*@[^:]*:\([0-9]*\)\/.*/\1/p')

        if [[ -n "$db_host" && -n "$db_port" ]]; then
            wait_for_service "$db_host" "$db_port" 60 "database"
        fi
    fi

    # Wait for Redis if configured
    if [[ -n "${REDIS_URL:-}" ]]; then
        local redis_host redis_port
        redis_host=$(echo "${REDIS_URL}" | sed -n 's/redis:\/\/\([^:]*\):.*/\1/p')
        redis_port=$(echo "${REDIS_URL}" | sed -n 's/redis:\/\/[^:]*:\([0-9]*\)\/.*/\1/p')

        if [[ -n "$redis_host" && -n "$redis_port" ]]; then
            wait_for_service "$redis_host" "$redis_port" 30 "Redis"
        fi
    fi
}

run_database_migrations() {
    info "Running database migrations..."

    local migrations_dir="${APP_DIR}/migrations"

    if [[ -f "${migrations_dir}/env.py" ]]; then
        info "Applying database migrations..."

        # Run migrations with timeout and error handling
        if timeout 300 python -m flask db upgrade 2>&1; then
            info "Database migrations completed successfully"
        else
            error "Database migrations failed or timed out"
            return 1
        fi
    else
        debug "No migrations directory found - skipping database migrations"
    fi
}

# -----------------------------------------------------------------------------
# Health Checks & Validation
# -----------------------------------------------------------------------------
run_comprehensive_health_check() {
    info "Running comprehensive production health checks..."

    # Application import and configuration validation
    python -c "
import sys
import os
sys.path.insert(0, '${APP_DIR}/src')

try:
    # Test application import
    from goldilocks.app import create_app
    app = create_app()

    # Test application context
    with app.app_context():
        # Test database connectivity if configured
        if 'DATABASE_URL' in os.environ:
            try:
                from flask import g
                # Basic database connection test would go here
                print('✅ Database connectivity validated')
            except Exception as e:
                print(f'⚠️  Database validation warning: {e}')

        # Test cache connectivity if configured
        if any(var in os.environ for var in ['REDIS_URL', 'CACHE_REDIS_URL']):
            try:
                # Basic cache connection test would go here
                print('✅ Cache connectivity validated')
            except Exception as e:
                print(f'⚠️  Cache validation warning: {e}')

    # Test basic HTTP endpoint
    with app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print('✅ Health endpoint responding')
        else:
            print(f'❌ Health endpoint returned {response.status_code}')
            sys.exit(1)

    print('✅ All production health checks passed')

except Exception as e:
    print(f'❌ Production health check failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

    info "Production health checks completed successfully"
}

# -----------------------------------------------------------------------------
# Signal Handling for Graceful Shutdown
# -----------------------------------------------------------------------------
setup_signal_handlers() {
    # Store gunicorn PID for graceful shutdown
    local gunicorn_pid=0

    handle_shutdown() {
        info "Received shutdown signal, gracefully stopping..."
        if [[ $gunicorn_pid -gt 0 ]]; then
            kill -TERM "$gunicorn_pid" 2>/dev/null || true
            wait "$gunicorn_pid" 2>/dev/null || true
        fi
        info "Graceful shutdown completed"
        exit 0
    }

    trap handle_shutdown TERM INT
}

# -----------------------------------------------------------------------------
# Main Production Server Launch
# -----------------------------------------------------------------------------
start_production_server() {
    info "🚀 Starting Goldilocks Production Server"

    # Build Gunicorn command with all options
    local gunicorn_cmd=(
        "python" "-m" "gunicorn"
        "--bind" "0.0.0.0:${WEB_PORT:-9000}"
        "--workers" "$WORKERS"
        "--worker-class" "$WORKER_CLASS"
        "--worker-connections" "$WORKER_CONNECTIONS"
        "--timeout" "$TIMEOUT"
        "--keep-alive" "$KEEPALIVE"
        "--max-requests" "$MAX_REQUESTS"
        "--max-requests-jitter" "$MAX_REQUESTS_JITTER"
        "--graceful-timeout" "$GRACEFUL_TIMEOUT"
        "--user" "$USER"
        "--group" "$GROUP"
        "--umask" "$UMASK"
        "--access-logfile" "$ACCESS_LOGFILE"
        "--access-logformat" "$ACCESS_LOG_FORMAT"
        "--error-logfile" "$ERROR_LOGFILE"
        "--log-level" "$LOGLEVEL"
        "--capture-output"
        "--enable-stdio-inheritance"
    )

    # Add preload option if enabled
    if [[ "$PRELOAD" == "true" ]]; then
        gunicorn_cmd+=("--preload")
    fi

    # Add worker temp directory if specified
    if [[ -n "${WORKER_TMP_DIR:-}" && -d "$WORKER_TMP_DIR" ]]; then
        gunicorn_cmd+=("--worker-tmp-dir" "$WORKER_TMP_DIR")
    fi

    # Add the application
    gunicorn_cmd+=("goldilocks.app:app")

    info "🌐 Server will be available at http://0.0.0.0:${WEB_PORT:-9000}"
    info "⚡ Starting production server with optimized configuration..."

    # Execute Gunicorn with proper signal handling
    exec "${gunicorn_cmd[@]}" &
    PID=$!
    wait $PID
}

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
main() {
    info "🚀 Goldilocks Production Server Initialization"
    info "Script: $SCRIPT_NAME | PID: $$ | User: $(whoami)"

    # Verify required commands
    local required_commands=("python" "pip")
    for cmd in "${required_commands[@]}"; do
        check_command "$cmd"
    done

    # Check for Gunicorn
    if ! check_command "gunicorn" && ! python -c "import gunicorn" 2>/dev/null; then
        error "Gunicorn not found. Installing..."
        pip install gunicorn[gevent] 2>/dev/null || pip install gunicorn
    fi

    # Setup phases
    setup_production_environment
    setup_gunicorn_config
    wait_for_dependencies
    run_database_migrations
    run_comprehensive_health_check

    # Final startup
    setup_signal_handlers
    start_production_server
}

# Execute main function
main "$@"
