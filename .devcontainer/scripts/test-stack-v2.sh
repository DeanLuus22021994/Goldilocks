#!/usr/bin/env bash
# ==============================================================================
# Goldilocks Stack Ultra-Reliable Comprehensive Test Suite
# Tests all services, dependencies, health checks, and configurations
# Designed for maximum reliability in DevContainer environments
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

# Configuration - Ultra-reliable path resolution
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
readonly DOCKER_DIR="${PROJECT_ROOT}/infrastructure/docker"
readonly COMPOSE_FILE="${DOCKER_DIR}/docker-compose.yml"
readonly TEST_TIMEOUT=300
readonly HEALTH_CHECK_RETRIES=30
readonly HEALTH_CHECK_INTERVAL=5

# Validate environment before starting
validate_environment() {
    echo "🔍 Validating test environment..."

    # Check required files
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        echo "❌ ERROR: Docker Compose file not found at $COMPOSE_FILE" >&2
        exit 1
    fi

    # Check Docker availability
    if ! command -v docker &> /dev/null; then
        echo "❌ ERROR: Docker command not found" >&2
        exit 1
    fi

    # Check if we can connect to Docker
    if ! docker info &> /dev/null; then
        echo "❌ ERROR: Cannot connect to Docker daemon" >&2
        exit 1
    fi

    echo "✅ Environment validation passed"
}

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Logging functions with enhanced reliability
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    ((PASSED_TESTS++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ((FAILED_TESTS++))
}

log_step() {
    echo ""
    echo -e "${PURPLE}==== $1 ====${NC}"
}

log_test() {
    echo -e "${CYAN}[TEST]${NC} $1"
    ((TOTAL_TESTS++))
}

# Enhanced wait function with better error handling
wait_for_service() {
    local service_name="$1"
    local max_attempts="$2"
    local test_command="$3"
    local attempt=1

    log_info "Waiting for $service_name (max $max_attempts attempts)..."

    while [[ $attempt -le $max_attempts ]]; do
        if eval "$test_command" &>/dev/null; then
            log_success "$service_name is ready (attempt $attempt/$max_attempts)"
            return 0
        fi

        log_info "Attempt $attempt/$max_attempts failed, waiting ${HEALTH_CHECK_INTERVAL}s..."
        sleep "$HEALTH_CHECK_INTERVAL"
        ((attempt++))
    done

    log_error "$service_name failed to become ready after $max_attempts attempts"
    return 1
}

# Test Docker Compose services with absolute reliability
test_compose_services() {
    log_step "TESTING DOCKER COMPOSE SERVICES"

    log_test "Verifying Docker Compose file accessibility"
    if [[ ! -r "$COMPOSE_FILE" ]]; then
        log_error "Cannot read Docker Compose file at $COMPOSE_FILE"
        return 1
    fi
    log_success "Docker Compose file is accessible"

    log_test "Checking Docker Compose service status"
    local services_output
    if ! services_output=$(docker compose -f "$COMPOSE_FILE" ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null); then
        log_error "Failed to get Docker Compose service status"
        return 1
    fi

    echo "Docker Compose Services Status:"
    echo "$services_output"
    echo ""

    # Check if all expected services are running
    local expected_services=("goldilocks-backend" "goldilocks-db" "goldilocks-redis" "goldilocks-adminer" "goldilocks-frontend" "goldilocks-extensions")

    for service in "${expected_services[@]}"; do
        log_test "Verifying $service is running"
        if echo "$services_output" | grep -q "$service.*Up"; then
            log_success "$service is running"
        else
            log_error "$service is not running"
        fi
    done
}

# Test service health checks with enhanced validation
test_service_health() {
    log_step "TESTING SERVICE HEALTH CHECKS"

    # Test Redis connectivity
    log_test "Testing Redis connectivity"
    if wait_for_service "Redis" 10 "docker exec goldilocks-redis redis-cli ping"; then
        local redis_response
        if redis_response=$(docker exec goldilocks-redis redis-cli ping 2>/dev/null); then
            if [[ "$redis_response" == "PONG" ]]; then
                log_success "Redis responds with PONG"
            else
                log_error "Redis unexpected response: $redis_response"
            fi
        else
            log_error "Failed to get Redis response"
        fi
    fi

    # Test Redis Python connectivity (the critical fix)
    log_test "Testing Redis Python package connectivity"
    local redis_python_test='python -c "import redis; r=redis.Redis(host=\"goldilocks-redis\", port=6379, db=0, socket_connect_timeout=5); print(r.ping()); r.close()"'
    if wait_for_service "Redis Python" 10 "docker exec goldilocks-backend bash -c \"$redis_python_test\""; then
        local redis_py_response
        if redis_py_response=$(docker exec goldilocks-backend bash -c "$redis_python_test" 2>/dev/null); then
            if [[ "$redis_py_response" == "True" ]]; then
                log_success "Redis Python package connectivity confirmed"
            else
                log_error "Redis Python package unexpected response: $redis_py_response"
            fi
        else
            log_error "Failed to test Redis Python connectivity"
        fi
    fi

    # Test MariaDB connectivity
    log_test "Testing MariaDB connectivity"
    local db_test_command='python -c "import pymysql; conn=pymysql.connect(host=\"goldilocks-db\", user=\"goldilocks_app\", password=\"goldilocks_app_secure_2024\", database=\"goldilocks\"); print(\"Connected\"); conn.close()"'

    if wait_for_service "MariaDB" 15 "docker exec goldilocks-backend bash -c \"$db_test_command\""; then
        local db_response
        if db_response=$(docker exec goldilocks-backend bash -c "$db_test_command" 2>/dev/null); then
            if [[ "$db_response" == "Connected" ]]; then
                log_success "MariaDB connection successful"
            else
                log_error "MariaDB connection failed: $db_response"
            fi
        else
            log_error "Failed to test MariaDB connectivity"
        fi
    fi

    # Test Docker health checks
    log_test "Checking Docker health status for all services"
    local health_output
    if ! health_output=$(docker compose -f "$COMPOSE_FILE" ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null); then
        log_error "Failed to get Docker health status"
        return 1
    fi

    while IFS=$'\t' read -r name status; do
        if [[ "$name" == "NAME" ]] || [[ -z "$name" ]]; then continue; fi

        log_test "Health check for $name"
        if echo "$status" | grep -q "healthy\|Up.*seconds"; then
            log_success "$name is healthy"
        elif echo "$status" | grep -q "starting"; then
            log_warning "$name is still starting up"
        else
            log_error "$name health check failed: $status"
        fi
    done <<< "$health_output"
}

# Test HTTP endpoints with comprehensive validation
test_http_endpoints() {
    log_step "TESTING HTTP ENDPOINTS"

    # Test Flask backend health endpoint
    log_test "Testing Flask /health endpoint"
    if wait_for_service "Flask health endpoint" 20 "curl -sf http://localhost:9000/health"; then
        local health_response
        if health_response=$(curl -sf http://localhost:9000/health 2>/dev/null); then
            if echo "$health_response" | grep -q '"status".*"ok"'; then
                log_success "Flask /health endpoint responds correctly"
                echo "Response: $health_response"
            else
                log_error "Flask /health endpoint unexpected response: $health_response"
            fi
        else
            log_error "Failed to get Flask health response"
        fi
    fi

    # Test Flask version endpoint
    log_test "Testing Flask /version endpoint"
    if wait_for_service "Flask version endpoint" 10 "curl -sf http://localhost:9000/version"; then
        local version_response
        if version_response=$(curl -sf http://localhost:9000/version 2>/dev/null); then
            if echo "$version_response" | grep -q '"app".*"python".*"flask"'; then
                log_success "Flask /version endpoint responds correctly"
                echo "Response: $version_response"
            else
                log_error "Flask /version endpoint unexpected response: $version_response"
            fi
        else
            log_error "Failed to get Flask version response"
        fi
    fi

    # Test Adminer accessibility
    log_test "Testing Adminer web interface"
    if wait_for_service "Adminer web interface" 10 "curl -sf http://localhost:8080"; then
        log_success "Adminer web interface is accessible"
    fi
}

# Test jq availability and JSON parsing
test_jq_functionality() {
    log_step "TESTING JQ JSON PROCESSING"

    log_test "Testing jq availability in backend container"
    if docker exec goldilocks-backend which jq &>/dev/null; then
        log_success "jq is installed in backend container"

        # Test JSON parsing functionality
        log_test "Testing jq JSON parsing capability"
        local test_json='{"test": "value", "number": 42}'
        local jq_result
        if jq_result=$(docker exec goldilocks-backend bash -c "echo '$test_json' | jq .test" 2>/dev/null); then
            if [[ "$jq_result" == '"value"' ]]; then
                log_success "jq JSON parsing works correctly"
            else
                log_error "jq JSON parsing unexpected result: $jq_result"
            fi
        else
            log_error "Failed to test jq JSON parsing"
        fi
    else
        log_error "jq is not installed in backend container"
    fi
}

# Test devcontainer specific functionality
test_devcontainer_features() {
    log_step "TESTING DEVCONTAINER FEATURES"

    log_test "Testing Python environment in devcontainer"
    if docker exec goldilocks-backend python --version &>/dev/null; then
        local python_version
        python_version=$(docker exec goldilocks-backend python --version 2>/dev/null)
        log_success "Python is available: $python_version"
    else
        log_error "Python is not available in devcontainer"
    fi

    log_test "Testing Flask CLI availability"
    if docker exec goldilocks-backend flask --version &>/dev/null; then
        local flask_version
        flask_version=$(docker exec goldilocks-backend flask --version 2>/dev/null)
        log_success "Flask CLI is available: $flask_version"
    else
        log_error "Flask CLI is not available in devcontainer"
    fi

    log_test "Testing required Python packages"
    local required_packages=("flask" "redis" "pymysql")
    for package in "${required_packages[@]}"; do
        if docker exec goldilocks-backend python -c "import $package" &>/dev/null; then
            log_success "Python package '$package' is available"
        else
            log_error "Python package '$package' is not available"
        fi
    done
}

# Main test execution
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              GOLDILOCKS STACK TEST SUITE                     ║"
    echo "║                        ULTRA-RELIABLE                        ║"
    echo "║                                                              ║"
    echo "║  Comprehensive validation of all services, configurations,   ║"
    echo "║  health checks, connectivity, and functionality.             ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""

    # Validate environment first
    validate_environment

    log_info "Starting comprehensive stack testing..."
    log_info "Project root: $PROJECT_ROOT"
    log_info "Docker directory: $DOCKER_DIR"
    log_info "Compose file: $COMPOSE_FILE"
    log_info "Test timeout: ${TEST_TIMEOUT}s"
    log_info "Health check retries: $HEALTH_CHECK_RETRIES"
    log_info "Health check interval: ${HEALTH_CHECK_INTERVAL}s"
    echo ""

    # Execute all test suites
    test_compose_services
    test_service_health
    test_http_endpoints
    test_jq_functionality
    test_devcontainer_features

    # Final results
    echo ""
    log_step "TEST RESULTS SUMMARY"
    echo ""
    echo -e "${BLUE}Total tests executed:${NC} $TOTAL_TESTS"
    echo -e "${GREEN}Tests passed:${NC} $PASSED_TESTS"
    echo -e "${RED}Tests failed:${NC} $FAILED_TESTS"
    echo ""

    if [[ $FAILED_TESTS -eq 0 ]]; then
        echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║                                                              ║${NC}"
        echo -e "${GREEN}║                    🎉 ALL TESTS PASSED! 🎉                  ║${NC}"
        echo -e "${GREEN}║                                                              ║${NC}"
        echo -e "${GREEN}║  The Goldilocks stack is fully functional and reliable.     ║${NC}"
        echo -e "${GREEN}║  All services are healthy and all fixes are confirmed.      ║${NC}"
        echo -e "${GREEN}║                                                              ║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
        exit 0
    else
        echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║                                                              ║${NC}"
        echo -e "${RED}║                    ❌ TESTS FAILED ❌                        ║${NC}"
        echo -e "${RED}║                                                              ║${NC}"
        echo -e "${RED}║  Some issues were detected. Review the logs above.          ║${NC}"
        echo -e "${RED}║                                                              ║${NC}"
        echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
        exit 1
    fi
}

# Execute main function
main "$@"
