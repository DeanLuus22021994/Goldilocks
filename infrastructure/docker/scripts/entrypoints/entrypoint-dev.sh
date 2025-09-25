#!/bin/bash
# ==============================================================================
# Goldilocks Development Entrypoint Script
# MODERNIZE - Latest bash best practices and error handling
# STRUCTURED - Organized, maintainable script architecture
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
readonly CACHE_DIR="/tmp/goldilocks-cache"
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# -----------------------------------------------------------------------------
# Logging Functions
# -----------------------------------------------------------------------------
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date -Iseconds)

    case "$level" in
        INFO)  echo -e "${GREEN}[${timestamp}] [INFO]${NC} $message" ;;
        WARN)  echo -e "${YELLOW}[${timestamp}] [WARN]${NC} $message" ;;
        ERROR) echo -e "${RED}[${timestamp}] [ERROR]${NC} $message" >&2 ;;
        DEBUG) [[ "${LOG_LEVEL}" == "DEBUG" ]] && echo -e "${BLUE}[${timestamp}] [DEBUG]${NC} $message" ;;
    esac
}

info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; }
debug() { log "DEBUG" "$@"; }

# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        error "Script failed with exit code: $exit_code"
        error "Failed command was: $BASH_COMMAND"
    fi
    exit $exit_code
}

trap cleanup EXIT
trap 'error "Script interrupted"; exit 130' INT TERM

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
    local timeout="${3:-30}"
    local service_name="${4:-service}"

    info "Waiting for $service_name at $host:$port (timeout: ${timeout}s)"

    for i in $(seq 1 "$timeout"); do
        if timeout 3 bash -c "</dev/tcp/$host/$port" 2>/dev/null; then
            info "$service_name is ready!"
            return 0
        fi
        debug "Attempt $i/$timeout failed, retrying in 1 second..."
        sleep 1
    done

    error "$service_name at $host:$port is not available after ${timeout}s"
    return 1
}

create_directories() {
    local dirs=("$@")
    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            debug "Creating directory: $dir"
            mkdir -p "$dir"
        fi
    done
}

set_permissions() {
    local path="$1"
    local owner="${2:-app:app}"

    if [[ -e "$path" ]]; then
        debug "Setting ownership of $path to $owner"
        chown -R "$owner" "$path" 2>/dev/null || {
            warn "Could not change ownership of $path (running as non-privileged user?)"
        }
    fi
}

# -----------------------------------------------------------------------------
# Environment Setup Functions
# -----------------------------------------------------------------------------
setup_environment() {
    info "Setting up development environment..."

    # Activate virtual environment
    if [[ -f "${VENV_PATH}/bin/activate" ]]; then
        debug "Activating virtual environment: $VENV_PATH"
        # shellcheck source=/dev/null
        source "${VENV_PATH}/bin/activate"
    else
        warn "Virtual environment not found at $VENV_PATH"
    fi

    # Set Flask environment variables
    export FLASK_APP="${FLASK_APP:-goldilocks.app}"
    export FLASK_ENV="${FLASK_ENV:-development}"
    export FLASK_DEBUG="${FLASK_DEBUG:-1}"
    export FLASK_RUN_HOST="${FLASK_RUN_HOST:-0.0.0.0}"
    export FLASK_RUN_PORT="${FLASK_RUN_PORT:-9000}"

    # Python path configuration
    export PYTHONPATH="${APP_DIR}/src:${PYTHONPATH:-}"

    # Development performance optimizations
    export PYTHONUNBUFFERED=1
    export PYTHONDONTWRITEBYTECODE=0  # Keep .pyc for development debugging
    export PYTHONHASHSEED=0           # Reproducible hash seeds
    export FLASK_SKIP_DOTENV=1        # We manage env vars ourselves

    # Development-specific settings
    export TEMPLATES_AUTO_RELOAD=1
    export SEND_FILE_MAX_AGE_DEFAULT=1
    export EXPLAIN_TEMPLATE_LOADING=0

    debug "Environment variables configured successfully"
}

setup_cache_directories() {
    info "Setting up cache directories..."

    local cache_dirs=(
        "${CACHE_DIR}/pip"
        "${CACHE_DIR}/mypy"
        "${CACHE_DIR}/pytest"
        "${CACHE_DIR}/ruff"
        "${CACHE_DIR}/pre-commit"
        "${CACHE_DIR}/flask"
        "/tmp/prometheus_multiproc"
    )

    create_directories "${cache_dirs[@]}"
    set_permissions "$CACHE_DIR" "app:app"

    # Set cache environment variables
    export PIP_CACHE_DIR="${CACHE_DIR}/pip"
    export MYPY_CACHE_DIR="${CACHE_DIR}/mypy"
    export PYTEST_CACHE_DIR="${CACHE_DIR}/pytest"
    export PRE_COMMIT_HOME="${CACHE_DIR}/pre-commit"
    export PROMETHEUS_MULTIPROC_DIR="/tmp/prometheus_multiproc"

    debug "Cache directories configured successfully"
}

setup_git_permissions() {
    info "Configuring Git permissions for development..."

    local git_dir="/workspaces/Goldilocks/.git"

    if [[ -d "$git_dir" ]]; then
        debug "Found Git repository at $git_dir"

        # Fix ownership if running with privileges
        if [[ $(id -u) -eq 0 ]] || groups | grep -q sudo; then
            set_permissions "/workspaces/Goldilocks/.git" "app:app"
            chmod -R u+rw "/workspaces/Goldilocks/.git/" 2>/dev/null || true
        fi

        # Configure Git for container environment
        if command -v git >/dev/null 2>&1; then
            git config --global --add safe.directory /workspaces/Goldilocks 2>/dev/null || true
            git config --global init.defaultBranch main 2>/dev/null || true
            debug "Git configuration updated for container environment"
        fi
    else
        debug "No Git repository found (this is normal for some deployment scenarios)"
    fi
}

# -----------------------------------------------------------------------------
# Database Functions
# -----------------------------------------------------------------------------
run_database_migrations() {
    info "Checking for database migrations..."

    local migrations_dir="${APP_DIR}/migrations"

    if [[ -f "${migrations_dir}/env.py" ]]; then
        info "Running database migrations..."

        # Wait for database if URL contains a host
        if [[ "${DATABASE_URL:-}" == *"@"* ]]; then
            local db_host
            db_host=$(echo "${DATABASE_URL}" | sed -n 's/.*@\([^:]*\):.*/\1/p')
            local db_port
            db_port=$(echo "${DATABASE_URL}" | sed -n 's/.*@[^:]*:\([0-9]*\)\/.*/\1/p')

            if [[ -n "$db_host" && -n "$db_port" ]]; then
                wait_for_service "$db_host" "$db_port" 30 "database"
            fi
        fi

        # Run migrations with error handling
        if python -m flask db upgrade 2>&1; then
            info "Database migrations completed successfully"
        else
            warn "Database migrations failed or no migrations to run"
            # Don't exit on migration failure in development
        fi
    else
        debug "No migrations directory found at $migrations_dir"
    fi
}

# -----------------------------------------------------------------------------
# Health Check Functions
# -----------------------------------------------------------------------------
run_health_check() {
    info "Running application health check..."

    # Basic import check
    if ! python -c "
import sys
sys.path.insert(0, '${APP_DIR}/src')
try:
    from goldilocks.app import create_app
    app = create_app()
    print('✅ Application imports successful')
except Exception as e:
    print(f'❌ Application import failed: {e}')
    sys.exit(1)
" 2>&1; then
        error "Application health check failed - import errors detected"
        return 1
    fi

    # Configuration validation
    python -c "
import os
import sys
sys.path.insert(0, '${APP_DIR}/src')

required_vars = ['FLASK_APP', 'FLASK_ENV', 'PYTHONPATH']
missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    print(f'❌ Missing required environment variables: {missing_vars}')
    sys.exit(1)
else:
    print('✅ Environment configuration validated')
"

    info "Application health check passed"
}

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
main() {
    info "🚀 Starting Goldilocks Development Server"
    info "Script: $SCRIPT_NAME | PID: $$ | User: $(whoami)"

    # Verify required commands
    local required_commands=("python" "pip")
    for cmd in "${required_commands[@]}"; do
        check_command "$cmd"
    done

    # Setup phases
    setup_environment
    setup_cache_directories
    setup_git_permissions
    run_database_migrations
    run_health_check

    # Display configuration summary
    info "🔧 Development Server Configuration:"
    info "   Flask App: ${FLASK_APP}"
    info "   Environment: ${FLASK_ENV}"
    info "   Debug Mode: ${FLASK_DEBUG}"
    info "   Host: ${FLASK_RUN_HOST}:${FLASK_RUN_PORT}"
    info "   Python Path: ${PYTHONPATH}"
    info "   Cache Directory: ${CACHE_DIR}"

    # Start development server
    info "🔥 Starting Flask development server with hot reload..."
    info "🌐 Server will be available at http://${FLASK_RUN_HOST}:${FLASK_RUN_PORT}"

    # Use exec to replace shell process for proper signal handling
    exec python -m flask run \
        --host="${FLASK_RUN_HOST}" \
        --port="${FLASK_RUN_PORT}" \
        --reload \
        --debugger \
        --with-threads \
        --extra-files="${APP_DIR}/src" \
        2>&1
}

# Execute main function
main "$@"
