#!/bin/bash
# ==============================================================================
# Goldilocks Docker Compose Utility Script
# STRUCTURED - Centralized deployment management
# STANDARDIZATION - Consistent deployment commands
# HIGH COMPATIBILITY - Support for multiple environments
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

# Script configuration
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(dirname "$0")
readonly DOCKER_DIR="${SCRIPT_DIR}/.."
readonly PROJECT_NAME="goldilocks"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Logging functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date -Iseconds)

    case "$level" in
        INFO)  echo -e "${GREEN}[${timestamp}] [INFO]${NC} $message" ;;
        WARN)  echo -e "${YELLOW}[${timestamp}] [WARN]${NC} $message" ;;
        ERROR) echo -e "${RED}[${timestamp}] [ERROR]${NC} $message" >&2 ;;
        DEBUG) [[ "${DEBUG:-}" == "1" ]] && echo -e "${BLUE}[${timestamp}] [DEBUG]${NC} $message" ;;
    esac
}

info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; }
debug() { log "DEBUG" "$@"; }

# Environment configurations
declare -A ENVIRONMENTS=(
    ["development"]="compose/overrides/development.yml"
    ["production"]="compose/overrides/production.yml"
    ["testing"]="compose/overrides/testing.yml"
    ["ci-cd"]="compose/overrides/ci-cd.yml"
    ["edge"]="compose/overrides/edge.yml"
)

# Usage information
show_usage() {
    cat << EOF
${SCRIPT_NAME} - Goldilocks Docker Compose Management Tool

USAGE:
    ${SCRIPT_NAME} <command> [environment] [options]

COMMANDS:
    up          Start services
    down        Stop services
    restart     Restart services
    logs        Show service logs
    status      Show service status
    build       Build/rebuild services
    clean       Clean up containers, volumes, and images
    backup      Backup application data
    restore     Restore application data
    health      Check service health
    shell       Open shell in service container
    update      Update service images

ENVIRONMENTS:
    development    Local development with hot reload
    production     Production deployment
    testing        Testing environment
    ci-cd          CI/CD pipeline environment
    edge           Edge computing deployment

EXAMPLES:
    ${SCRIPT_NAME} up development
    ${SCRIPT_NAME} down production
    ${SCRIPT_NAME} logs development goldilocks-app
    ${SCRIPT_NAME} build production
    ${SCRIPT_NAME} backup production
    ${SCRIPT_NAME} health production

OPTIONS:
    -h, --help     Show this help message
    -v, --verbose  Enable verbose output
    -d, --detach   Run in detached mode (for up command)
    --no-cache     Don't use cache when building
    --pull         Always pull latest images

EOF
}

# Validate environment
validate_environment() {
    local env="$1"
    if [[ -z "${ENVIRONMENTS[$env]:-}" ]]; then
        error "Invalid environment: $env"
        error "Available environments: ${!ENVIRONMENTS[*]}"
        exit 1
    fi
}

# Get compose files for environment
get_compose_files() {
    local env="$1"
    local files=("-f" "docker-compose.yml")

    if [[ -n "${ENVIRONMENTS[$env]:-}" ]]; then
        files+=("-f" "${ENVIRONMENTS[$env]}")
    fi

    echo "${files[@]}"
}

# Execute docker-compose command
execute_compose() {
    local env="$1"
    shift
    local compose_files
    read -ra compose_files <<< "$(get_compose_files "$env")"

    debug "Executing: docker-compose ${compose_files[*]} $*"
    cd "$DOCKER_DIR" || exit 1
    docker-compose "${compose_files[@]}" "$@"
}

# Command implementations
cmd_up() {
    local env="$1"
    shift
    local args=("$@")

    info "Starting Goldilocks services for environment: $env"

    if [[ "${DETACH:-}" == "1" ]]; then
        args+=("-d")
    fi

    execute_compose "$env" up "${args[@]}"

    if [[ "$env" == "development" ]]; then
        info "Development environment started!"
        info "Application: http://localhost:9000"
        info "Database Admin: http://localhost:8080"
    fi
}

cmd_down() {
    local env="$1"
    shift

    info "Stopping Goldilocks services for environment: $env"
    execute_compose "$env" down "$@"
}

cmd_restart() {
    local env="$1"
    shift

    info "Restarting Goldilocks services for environment: $env"
    execute_compose "$env" restart "$@"
}

cmd_logs() {
    local env="$1"
    shift

    info "Showing logs for environment: $env"
    execute_compose "$env" logs -f "$@"
}

cmd_status() {
    local env="$1"

    info "Service status for environment: $env"
    execute_compose "$env" ps
}

cmd_build() {
    local env="$1"
    shift
    local args=("$@")

    info "Building services for environment: $env"

    if [[ "${NO_CACHE:-}" == "1" ]]; then
        args+=("--no-cache")
    fi

    if [[ "${PULL:-}" == "1" ]]; then
        args+=("--pull")
    fi

    execute_compose "$env" build "${args[@]}"
}

cmd_clean() {
    local env="$1"

    warn "This will remove all containers, volumes, and images for environment: $env"
    read -p "Are you sure? [y/N] " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        info "Cleaning up environment: $env"
        execute_compose "$env" down -v --remove-orphans
        docker system prune -f
        info "Cleanup completed"
    else
        info "Cleanup cancelled"
    fi
}

cmd_health() {
    local env="$1"

    info "Checking health for environment: $env"

    # Get container health status
    local containers
    mapfile -t containers < <(execute_compose "$env" ps -q)

    for container in "${containers[@]}"; do
        if [[ -n "$container" ]]; then
            local name
            name=$(docker inspect --format '{{.Name}}' "$container" | sed 's/^.//')
            local health
            health=$(docker inspect --format '{{.State.Health.Status}}' "$container" 2>/dev/null || echo "no-health-check")

            case "$health" in
                "healthy")
                    info "✅ $name: healthy"
                    ;;
                "unhealthy")
                    error "❌ $name: unhealthy"
                    ;;
                "starting")
                    warn "🔄 $name: starting"
                    ;;
                "no-health-check")
                    info "➖ $name: no health check configured"
                    ;;
                *)
                    warn "❓ $name: unknown health status ($health)"
                    ;;
            esac
        fi
    done
}

cmd_shell() {
    local env="$1"
    local service="${2:-goldilocks-app}"

    info "Opening shell in $service for environment: $env"
    execute_compose "$env" exec "$service" /bin/bash
}

# Main execution
main() {
    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--verbose)
                export DEBUG=1
                shift
                ;;
            -d|--detach)
                export DETACH=1
                shift
                ;;
            --no-cache)
                export NO_CACHE=1
                shift
                ;;
            --pull)
                export PULL=1
                shift
                ;;
            -*)
                error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                break
                ;;
        esac
    done

    # Require command
    if [[ $# -lt 1 ]]; then
        error "Command required"
        show_usage
        exit 1
    fi

    local command="$1"
    shift

    # Require environment for most commands
    if [[ $# -lt 1 && "$command" != "clean" ]]; then
        error "Environment required"
        show_usage
        exit 1
    fi

    local environment="${1:-}"
    if [[ -n "$environment" ]]; then
        validate_environment "$environment"
        shift
    fi

    # Execute command
    case "$command" in
        up)
            cmd_up "$environment" "$@"
            ;;
        down)
            cmd_down "$environment" "$@"
            ;;
        restart)
            cmd_restart "$environment" "$@"
            ;;
        logs)
            cmd_logs "$environment" "$@"
            ;;
        status)
            cmd_status "$environment"
            ;;
        build)
            cmd_build "$environment" "$@"
            ;;
        clean)
            cmd_clean "$environment"
            ;;
        health)
            cmd_health "$environment"
            ;;
        shell)
            cmd_shell "$environment" "$@"
            ;;
        *)
            error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
