#!/bin/bash
# ==============================================================================
# Goldilocks Docker Infrastructure Test Suite
# STRUCTURED - Comprehensive testing following standardized practices
# RELIABILITY - Validates entire infrastructure stack
# ==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$DOCKER_DIR")")")"
COMPOSE_FILE="$DOCKER_DIR/docker-compose.yml"

# Test configuration
TEST_TIMEOUT=300
HEALTH_CHECK_RETRIES=30
HEALTH_CHECK_INTERVAL=5

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${BLUE}==== $1 ====${NC}"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up test environment..."
    cd "$DOCKER_DIR" || exit 1
    docker compose down --volumes --remove-orphans 2>/dev/null || true
    docker volume prune -f 2>/dev/null || true
    docker network prune -f 2>/dev/null || true
}

# Error handler
error_handler() {
    log_error "Test failed at line $1"
    cleanup
    exit 1
}

# Set error trap
trap 'error_handler $LINENO' ERR

# Validate environment
validate_environment() {
    log_step "VALIDATING ENVIRONMENT"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi

    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available"
        exit 1
    fi

    # Check compose file exists
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Docker Compose file not found: $COMPOSE_FILE"
        exit 1
    fi

    log_success "Environment validation passed"
}

# Test compose file syntax
test_compose_syntax() {
    log_step "TESTING COMPOSE SYNTAX"

    cd "$DOCKER_DIR" || exit 1

    log_info "Validating compose file syntax..."
    if docker compose config > /dev/null; then
        log_success "Compose file syntax is valid"
    else
        log_error "Compose file syntax validation failed"
        return 1
    fi
}

# Test shared infrastructure components
test_shared_components() {
    log_step "TESTING SHARED COMPONENTS"

    cd "$DOCKER_DIR" || exit 1

    # Test networks
    log_info "Testing network configurations..."
    if docker compose -f compose/shared/networks.yml config > /dev/null 2>&1; then
        log_success "Networks configuration is valid"
    else
        log_error "Networks configuration failed"
        return 1
    fi

    # Test volumes
    log_info "Testing volume configurations..."
    if docker compose -f compose/shared/volumes.yml config > /dev/null 2>&1; then
        log_success "Volumes configuration is valid"
    else
        log_error "Volumes configuration failed"
        return 1
    fi

    # Test secrets
    log_info "Testing secrets configurations..."
    if docker compose -f compose/shared/secrets.yml config > /dev/null 2>&1; then
        log_success "Secrets configuration is valid"
    else
        log_error "Secrets configuration failed"
        return 1
    fi
}

# Test service definitions
test_service_definitions() {
    log_step "TESTING SERVICE DEFINITIONS"

    cd "$DOCKER_DIR" || exit 1

    local services=("database.yml" "backend.yml" "frontend.yml" "adminer.yml")

    for service in "${services[@]}"; do
        local service_file="compose/services/$service"
        log_info "Testing $service..."

        if [[ -f "$service_file" ]]; then
            if docker compose -f "$service_file" config > /dev/null 2>&1; then
                log_success "$service is valid"
            else
                log_error "$service configuration failed"
                return 1
            fi
        else
            log_warning "$service not found, skipping..."
        fi
    done
}

# Test environment overrides
test_environment_overrides() {
    log_step "TESTING ENVIRONMENT OVERRIDES"

    cd "$DOCKER_DIR" || exit 1

    local overrides=("development.yml" "production.yml" "ci-cd.yml")

    for override in "${overrides[@]}"; do
        local override_file="compose/overrides/$override"
        log_info "Testing $override..."

        if [[ -f "$override_file" ]]; then
            if docker compose -f docker-compose.yml -f "$override_file" config > /dev/null 2>&1; then
                log_success "$override is valid"
            else
                log_error "$override configuration failed"
                return 1
            fi
        else
            log_warning "$override not found, skipping..."
        fi
    done
}

# Test development environment
test_development_environment() {
    log_step "TESTING DEVELOPMENT ENVIRONMENT"

    cd "$DOCKER_DIR" || exit 1

    # Set environment variables for testing
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    export GOLDILOCKS_PROFILE=dev

    # Create shared components
    log_info "Creating shared infrastructure..."
    docker network create goldilocks-app-network --driver bridge || true

    # Start database first
    log_info "Starting database service..."
    docker compose up -d goldilocks-db

    # Wait for database health check
    log_info "Waiting for database to be healthy..."
    local retries=0
    while [[ $retries -lt $HEALTH_CHECK_RETRIES ]]; do
        if docker compose ps goldilocks-db | grep -q "healthy"; then
            log_success "Database is healthy"
            break
        fi

        log_info "Waiting for database... ($((retries + 1))/$HEALTH_CHECK_RETRIES)"
        sleep $HEALTH_CHECK_INTERVAL
        retries=$((retries + 1))
    done

    if [[ $retries -eq $HEALTH_CHECK_RETRIES ]]; then
        log_error "Database failed to become healthy"
        return 1
    fi

    # Test database connection
    log_info "Testing database connection..."
    if docker compose exec -T goldilocks-db healthcheck.sh --connect; then
        log_success "Database connection test passed"
    else
        log_error "Database connection test failed"
        return 1
    fi

    # Start additional services
    log_info "Starting additional services..."
    docker compose up -d goldilocks-adminer

    # Wait for all services
    sleep 10

    # Check service status
    log_info "Checking service status..."
    docker compose ps

    log_success "Development environment test completed"
}

# Test production-like environment
test_production_environment() {
    log_step "TESTING PRODUCTION-LIKE ENVIRONMENT"

    cd "$DOCKER_DIR" || exit 1

    # Cleanup first
    docker compose down --volumes --remove-orphans 2>/dev/null || true

    # Set production-like environment
    export GOLDILOCKS_PROFILE=prod
    export NODE_ENV=production
    export FLASK_ENV=production

    log_info "Testing production configuration..."
    if docker compose -f docker-compose.yml -f compose/overrides/production.yml config > /dev/null; then
        log_success "Production configuration is valid"
    else
        log_error "Production configuration failed"
        return 1
    fi

    log_success "Production environment test completed"
}

# Test volume management
test_volume_management() {
    log_step "TESTING VOLUME MANAGEMENT"

    cd "$DOCKER_DIR" || exit 1

    log_info "Testing volume creation..."
    docker compose up --no-start

    # List created volumes
    log_info "Checking created volumes..."
    local volumes
    volumes=$(docker volume ls --format "table {{.Name}}" | grep goldilocks || true)

    if [[ -n "$volumes" ]]; then
        log_success "Volumes created successfully:"
        echo "$volumes"
    else
        log_warning "No Goldilocks volumes found"
    fi

    # Test volume labeling
    log_info "Testing volume labels..."
    local labeled_volumes
    labeled_volumes=$(docker volume ls --filter "label=com.docker.compose.project=goldilocks" --format "table {{.Name}}" || true)

    if [[ -n "$labeled_volumes" ]]; then
        log_success "Volume labeling is working"
    else
        log_warning "Volume labeling may not be working properly"
    fi
}

# Test network configuration
test_network_configuration() {
    log_step "TESTING NETWORK CONFIGURATION"

    cd "$DOCKER_DIR" || exit 1

    log_info "Testing network creation..."
    docker compose up --no-start

    # Check network exists
    if docker network ls | grep -q goldilocks-app-network; then
        log_success "Application network created successfully"
    else
        log_error "Application network not found"
        return 1
    fi

    # Test network configuration
    log_info "Inspecting network configuration..."
    local network_info
    network_info=$(docker network inspect goldilocks-app-network --format '{{.IPAM.Config}}' || true)

    if [[ -n "$network_info" ]]; then
        log_success "Network configuration: $network_info"
    else
        log_warning "Could not retrieve network configuration"
    fi
}

# Performance benchmark
performance_benchmark() {
    log_step "PERFORMANCE BENCHMARK"

    cd "$DOCKER_DIR" || exit 1

    # Time the startup
    log_info "Benchmarking startup time..."
    local start_time
    start_time=$(date +%s)

    docker compose up -d goldilocks-db

    # Wait for healthy state
    local retries=0
    while [[ $retries -lt $HEALTH_CHECK_RETRIES ]]; do
        if docker compose ps goldilocks-db | grep -q "healthy"; then
            break
        fi
        sleep 1
        retries=$((retries + 1))
    done

    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log_success "Database startup time: ${duration}s"

    if [[ $duration -lt 60 ]]; then
        log_success "Startup performance is excellent"
    elif [[ $duration -lt 120 ]]; then
        log_warning "Startup performance is acceptable"
    else
        log_error "Startup performance needs optimization"
    fi
}

# Generate test report
generate_report() {
    log_step "GENERATING TEST REPORT"

    local report_file="$DOCKER_DIR/test-report-$(date +%Y%m%d_%H%M%S).txt"

    {
        echo "Goldilocks Docker Infrastructure Test Report"
        echo "==========================================="
        echo "Generated: $(date)"
        echo "Test Duration: $(($(date +%s) - test_start_time))s"
        echo ""
        echo "Environment Information:"
        echo "- Docker Version: $(docker --version)"
        echo "- Docker Compose Version: $(docker compose version --short)"
        echo "- OS: $(uname -s -r)"
        echo ""
        echo "Services Status:"
        cd "$DOCKER_DIR" || exit 1
        docker compose ps || true
        echo ""
        echo "Volume Information:"
        docker volume ls --filter "label=com.docker.compose.project=goldilocks" || true
        echo ""
        echo "Network Information:"
        docker network ls | grep goldilocks || true
    } > "$report_file"

    log_success "Test report generated: $report_file"
}

# Main test execution
main() {
    local test_start_time
    test_start_time=$(date +%s)

    log_step "STARTING GOLDILOCKS DOCKER INFRASTRUCTURE TESTS"
    log_info "Test suite started at $(date)"

    # Cleanup at start
    cleanup

    # Run test phases
    validate_environment
    test_compose_syntax
    test_shared_components
    test_service_definitions
    test_environment_overrides
    test_development_environment
    test_volume_management
    test_network_configuration
    performance_benchmark
    test_production_environment

    # Generate report
    generate_report

    # Final cleanup
    cleanup

    local total_duration=$(($(date +%s) - test_start_time))
    log_success "ALL TESTS COMPLETED SUCCESSFULLY in ${total_duration}s"
    log_info "Docker infrastructure is ready for production use"
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
