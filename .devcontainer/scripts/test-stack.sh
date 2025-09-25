#!/bin/bash
# ==============================================================================
# Goldilocks Stack Comprehensive Test Suite
# Tests all services, dependencies, health checks, and configurations
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

# Script configuration
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(dirname "$0")
readonly PROJECT_ROOT="/workspaces/Goldilocks"
readonly DOCKER_DIR="${PROJECT_ROOT}/infrastructure/docker"
readonly TEST_TIMEOUT=300
readonly HEALTH_CHECK_RETRIES=30
readonly HEALTH_CHECK_INTERVAL=5

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

# Logging functions
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

log_test() {
    echo -e "${PURPLE}[TEST]${NC} $1"
    ((TOTAL_TESTS++))
}

log_step() {
    echo -e "\n${CYAN}==== $1 ====${NC}"
}

# Utility functions
wait_for_service() {
    local service_name="$1"
    local max_attempts="$2"
    local check_command="$3"

    log_info "Waiting for $service_name to be ready..."

    for ((i=1; i<=max_attempts; i++)); do
        if eval "$check_command" &>/dev/null; then
            log_success "$service_name is ready (attempt $i/$max_attempts)"
            return 0
        fi

        if [ $i -lt $max_attempts ]; then
            log_info "Attempt $i/$max_attempts failed, retrying in ${HEALTH_CHECK_INTERVAL}s..."
            sleep $HEALTH_CHECK_INTERVAL
        fi
    done

    log_error "$service_name failed to become ready after $max_attempts attempts"
    return 1
}

# Test Docker Compose services
test_compose_services() {
    log_step "TESTING DOCKER COMPOSE SERVICES"

    log_test "Checking Docker Compose service status"

    local services_output
    services_output=$(docker compose -f "$DOCKER_DIR/docker-compose.yml" ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}")
    echo "$services_output"

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

# Test service health checks
test_service_health() {
    log_step "TESTING SERVICE HEALTH CHECKS"

    # Test Redis
    log_test "Testing Redis connectivity"
    if wait_for_service "Redis" 10 "docker exec goldilocks-redis redis-cli ping"; then
        local redis_response
        redis_response=$(docker exec goldilocks-redis redis-cli ping 2>/dev/null)
        if [ "$redis_response" = "PONG" ]; then
            log_success "Redis responds with PONG"
        else
            log_error "Redis unexpected response: $redis_response"
        fi
    fi

    # Test MariaDB
    log_test "Testing MariaDB connectivity"
    local db_test_command='python -c "import pymysql; conn=pymysql.connect(host=\"goldilocks-db\", user=\"goldilocks_app\", password=\"goldilocks_app_secure_2024\", database=\"goldilocks\"); print(\"Connected\"); conn.close()"'

    if wait_for_service "MariaDB" 15 "docker exec goldilocks-backend $db_test_command"; then
        local db_response
        db_response=$(docker exec goldilocks-backend bash -c "$db_test_command" 2>/dev/null)
        if [ "$db_response" = "Connected" ]; then
            log_success "MariaDB connection successful"
        else
            log_error "MariaDB connection failed: $db_response"
        fi
    fi

    # Test Docker health checks
    log_test "Checking Docker health status for all services"
    local health_output
    health_output=$(docker compose -f "$DOCKER_DIR/docker-compose.yml" ps --format "table {{.Name}}\t{{.Status}}")

    while IFS=$'\t' read -r name status; do
        if [[ "$name" == "NAME" ]]; then continue; fi
        if [[ -z "$name" ]]; then continue; fi

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

# Test Flask application
test_flask_application() {
    log_step "TESTING FLASK APPLICATION"

    # First, ensure Flask is running
    log_test "Starting Flask application if not running"
    local flask_processes
    flask_processes=$(docker exec goldilocks-backend pgrep -f flask || echo "")

    if [ -z "$flask_processes" ]; then
        log_info "Starting Flask application..."
        docker exec -d goldilocks-backend bash -c "export PATH=/opt/venv/bin:\$PATH && cd /workspaces/Goldilocks && flask run --host 0.0.0.0 --port 9000 --reload --debugger" || true
        sleep 10
    else
        log_info "Flask application already running (PID: $flask_processes)"
    fi

    # Wait for Flask to be ready
    if wait_for_service "Flask" 20 "curl -s -f http://localhost:9000/health"; then
        # Test health endpoint
        log_test "Testing Flask health endpoint"
        local health_response
        health_response=$(curl -s http://localhost:9000/health)
        local health_status
        health_status=$(echo "$health_response" | jq -r '.status' 2>/dev/null || echo "unknown")

        if [ "$health_status" = "ok" ]; then
            log_success "Flask health endpoint responds correctly"
            log_info "Health response: $health_response"
        else
            log_error "Flask health endpoint failed. Response: $health_response"
        fi

        # Test version endpoint
        log_test "Testing Flask version endpoint"
        local version_response
        version_response=$(curl -s http://localhost:9000/version)
        local flask_version
        flask_version=$(echo "$version_response" | jq -r '.flask' 2>/dev/null || echo "unknown")
        local python_version
        python_version=$(echo "$version_response" | jq -r '.python' 2>/dev/null || echo "unknown")

        if [ "$flask_version" != "unknown" ] && [ "$python_version" != "unknown" ]; then
            log_success "Flask version endpoint responds correctly"
            log_info "Flask version: $flask_version, Python version: $python_version"
        else
            log_error "Flask version endpoint failed. Response: $version_response"
        fi

        # Test index page
        log_test "Testing Flask index page"
        local index_status
        index_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/)

        if [ "$index_status" = "200" ]; then
            log_success "Flask index page responds with HTTP 200"
        else
            log_error "Flask index page failed with HTTP $index_status"
        fi

        # Test static files
        log_test "Testing Flask static file serving"
        local static_status
        static_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/static/css/base.css)

        if [ "$static_status" = "200" ] || [ "$static_status" = "304" ]; then
            log_success "Flask static file serving works (HTTP $static_status)"
        else
            log_warning "Flask static file test returned HTTP $static_status"
        fi
    fi
}

# Test VS Code extensions and MCP servers
test_extensions_and_mcp() {
    log_step "TESTING VS CODE EXTENSIONS AND MCP SERVERS"

    # Test extensions service
    log_test "Testing extensions service container"
    if docker exec goldilocks-extensions test -d /root/.vscode-server-insiders/extensions; then
        log_success "Extensions directory exists"
    else
        log_error "Extensions directory missing"
    fi

    if docker exec goldilocks-extensions test -d /root/.vscode-server-insiders/data; then
        log_success "VS Code Server data directory exists"
    else
        log_error "VS Code Server data directory missing"
    fi

    # Test Node.js and npm for MCP servers
    log_test "Testing Node.js availability for MCP servers"
    local node_version
    node_version=$(docker exec goldilocks-extensions node --version 2>/dev/null || echo "")

    if [ -n "$node_version" ]; then
        log_success "Node.js is available: $node_version"
    else
        log_error "Node.js is not available in extensions container"
    fi

    # Test Docker socket access for MCP servers
    log_test "Testing Docker socket access for MCP servers"
    if docker exec goldilocks-extensions test -S /var/run/docker.sock; then
        log_success "Docker socket is accessible"
    else
        log_error "Docker socket is not accessible"
    fi

    # Test MCP server packages
    log_test "Testing MCP server packages availability"
    local playwright_available
    playwright_available=$(docker exec goldilocks-extensions npm list -g @microsoft/mcp-server-playwright 2>/dev/null | grep -q "@microsoft/mcp-server-playwright" && echo "yes" || echo "no")

    if [ "$playwright_available" = "yes" ]; then
        log_success "MCP Playwright server is available"
    else
        log_warning "MCP Playwright server may not be installed"
    fi
}

# Test network connectivity between services
test_service_connectivity() {
    log_step "TESTING SERVICE CONNECTIVITY"

    # Test backend to database connectivity
    log_test "Testing backend to database connectivity"
    if docker exec goldilocks-backend ping -c 1 goldilocks-db >/dev/null 2>&1; then
        log_success "Backend can ping database"
    else
        log_error "Backend cannot ping database"
    fi

    # Test backend to Redis connectivity
    log_test "Testing backend to Redis connectivity"
    if docker exec goldilocks-backend ping -c 1 goldilocks-redis >/dev/null 2>&1; then
        log_success "Backend can ping Redis"
    else
        log_error "Backend cannot ping Redis"
    fi

    # Test Redis from backend using Redis client
    log_test "Testing Redis connectivity from backend"
    local redis_test_result
    redis_test_result=$(docker exec goldilocks-backend python -c "import redis; r=redis.Redis(host='goldilocks-redis', port=6379, decode_responses=True); r.ping(); print('OK')" 2>/dev/null || echo "FAILED")

    if [ "$redis_test_result" = "OK" ]; then
        log_success "Backend can connect to Redis via Python client"
    else
        log_error "Backend cannot connect to Redis via Python client"
    fi
}

# Test volume mounts and permissions
test_volumes_and_permissions() {
    log_step "TESTING VOLUMES AND PERMISSIONS"

    # Test workspace mount
    log_test "Testing workspace volume mount"
    if docker exec goldilocks-backend test -d /workspaces/Goldilocks; then
        log_success "Workspace directory is mounted"
    else
        log_error "Workspace directory is not mounted"
    fi

    # Test source code availability
    log_test "Testing source code availability"
    if docker exec goldilocks-backend test -f /workspaces/Goldilocks/src/goldilocks/app.py; then
        log_success "Source code is accessible"
    else
        log_error "Source code is not accessible"
    fi

    # Test cache volumes
    local cache_dirs=("/tmp/pip-cache" "/tmp/mypy-cache" "/tmp/ruff-cache" "/tmp/pytest-cache")

    for cache_dir in "${cache_dirs[@]}"; do
        log_test "Testing cache directory: $cache_dir"
        if docker exec goldilocks-backend test -d "$cache_dir"; then
            log_success "Cache directory exists: $cache_dir"
        else
            log_error "Cache directory missing: $cache_dir"
        fi
    done
}

# Test environment variables
test_environment_variables() {
    log_step "TESTING ENVIRONMENT VARIABLES"

    # Test Python environment variables
    log_test "Testing Python environment variables"
    local python_path
    python_path=$(docker exec goldilocks-backend printenv PYTHONPATH 2>/dev/null || echo "")

    if [[ "$python_path" == *"src"* ]]; then
        log_success "PYTHONPATH is configured correctly: $python_path"
    else
        log_error "PYTHONPATH is not configured correctly: $python_path"
    fi

    # Test Flask environment variables
    log_test "Testing Flask environment variables"
    local flask_app
    flask_app=$(docker exec goldilocks-backend printenv FLASK_APP 2>/dev/null || echo "")

    if [ "$flask_app" = "src.goldilocks.app" ]; then
        log_success "FLASK_APP is configured correctly: $flask_app"
    else
        log_error "FLASK_APP is not configured correctly: $flask_app"
    fi

    # Test database environment variables
    log_test "Testing database connection variables"
    local database_url
    database_url=$(docker exec goldilocks-backend printenv DATABASE_URL 2>/dev/null | sed 's/password=[^@]*/password=***/' || echo "")

    if [[ "$database_url" == *"goldilocks-db"* ]] && [[ "$database_url" == *"goldilocks"* ]]; then
        log_success "DATABASE_URL is configured correctly: $database_url"
    else
        log_error "DATABASE_URL is not configured correctly: $database_url"
    fi
}

# Generate test report
generate_test_report() {
    log_step "TEST REPORT SUMMARY"

    echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           TEST RESULTS               ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║ Total Tests:    ${TOTAL_TESTS}                   ║${NC}"
    echo -e "${CYAN}║ Passed:         ${GREEN}${PASSED_TESTS}${CYAN}                   ║${NC}"
    echo -e "${CYAN}║ Failed:         ${RED}${FAILED_TESTS}${CYAN}                   ║${NC}"

    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${CYAN}║ Status:         ${GREEN}ALL TESTS PASSED${CYAN}     ║${NC}"
        echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
        echo -e "\n${GREEN}🎉 GOLDILOCKS STACK IS FULLY FUNCTIONAL! 🎉${NC}\n"
        return 0
    else
        local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
        echo -e "${CYAN}║ Success Rate:   ${success_rate}%                 ║${NC}"
        echo -e "${CYAN}║ Status:         ${RED}SOME TESTS FAILED${CYAN}    ║${NC}"
        echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
        echo -e "\n${RED}⚠️  SOME TESTS FAILED - REVIEW ABOVE OUTPUT ⚠️${NC}\n"
        return 1
    fi
}

# Main execution
main() {
    echo -e "${PURPLE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              GOLDILOCKS STACK TEST SUITE                     ║
║                                                              ║
║  Comprehensive validation of all services, configurations,   ║
║  health checks, connectivity, and functionality.             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"

    log_info "Starting comprehensive stack testing..."
    log_info "Test timeout: ${TEST_TIMEOUT}s"
    log_info "Health check retries: ${HEALTH_CHECK_RETRIES}"
    log_info "Health check interval: ${HEALTH_CHECK_INTERVAL}s"

    # Run all test suites
    test_compose_services
    test_service_health
    test_flask_application
    test_extensions_and_mcp
    test_service_connectivity
    test_volumes_and_permissions
    test_environment_variables

    # Generate final report
    generate_test_report
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
