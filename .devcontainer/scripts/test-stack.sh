#!/usr/bin/env bash
# ==============================================================================
# Goldilocks Stack Ultra-Reliable Comprehensive Test Suite (Local Mode)
# Verifies the Flask application stack without Docker dependencies by
# validating the Python environment, running automated tests, and
# exercising critical HTTP endpoints via the Flask test client.
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

# Configuration - Ultra-reliable path resolution
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
readonly PYTHON_BIN="${PYTHON_BIN:-python3}"
readonly PYTEST_FLAGS="${PYTEST_FLAGS:--q}" # Allow callers to override verbosity

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

# Logging helpers -------------------------------------------------------------
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    ((PASSED_TESTS+=1))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ((FAILED_TESTS+=1))
}

log_step() {
    echo ""
    echo -e "${PURPLE}==== $1 ====${NC}"
}

log_test() {
    echo -e "${CYAN}[TEST]${NC} $1"
    ((TOTAL_TESTS+=1))
}

# Utility helpers -------------------------------------------------------------
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

python_module_available() {
    local module="$1"
    "$PYTHON_BIN" - <<PY >/dev/null 2>&1
import importlib.util
import sys

if importlib.util.find_spec("${module}") is None:
    sys.exit(1)
PY
}

run_python_snippet() {
    local description="$1"
    local script="$2"
    local output

    log_test "$description"
    if output=$("$PYTHON_BIN" - <<PY 2>&1
$script
PY
    ); then
        log_success "$description"
        [[ -n "$output" ]] && echo "$output"
    else
        log_error "$description failed"
        echo "$output"
    fi
}

run_command_test() {
    local description="$1"
    local working_dir="$2"
    shift 2
    local output

    log_test "$description"
    if [[ -z "$working_dir" || "$working_dir" == "." ]]; then
        if output=$("$@" 2>&1); then
            log_success "$description"
            [[ -n "$output" ]] && echo "$output"
        else
            log_error "$description failed"
            echo "$output"
        fi
        return
    fi

    if output=$(
        (
            cd "$working_dir" || exit 1
            "$@"
        ) 2>&1
    ); then
        log_success "$description"
        [[ -n "$output" ]] && echo "$output"
    else
        log_error "$description failed"
        echo "$output"
    fi
}

check_python_package() {
    local package="$1"
    log_test "Importing Python package '$package'"
    if "$PYTHON_BIN" -c "import ${package}" >/dev/null 2>&1; then
        log_success "Python package '$package' is available"
    else
        log_error "Python package '$package' is missing"
    fi
}

# Validation routines --------------------------------------------------------
validate_environment() {
    log_step "VALIDATING LOCAL ENVIRONMENT"

    # Ensure the Flask app boots in testing mode with isolated SQLite DB
    export FLASK_ENV="testing"
    export TEST_DATABASE_URL="${TEST_DATABASE_URL:-sqlite:///:memory:}"

    log_test "Ensuring Python interpreter '$PYTHON_BIN' is available"
    if command_exists "$PYTHON_BIN"; then
        if version_output=$("$PYTHON_BIN" --version 2>&1); then
            log_success "Python interpreter detected: $version_output"
        else
            log_error "Unable to determine Python version"
            exit 1
        fi
    else
        log_error "Python interpreter '$PYTHON_BIN' not found"
        exit 1
    fi

    log_test "Ensuring pytest is installed for '$PYTHON_BIN'"
    if "$PYTHON_BIN" -m pytest --version >/dev/null 2>&1; then
        log_success "pytest module detected"
    else
        log_error "pytest is required but not installed"
        exit 1
    fi

    log_test "Verifying Goldilocks package import"
    if "$PYTHON_BIN" -c "import goldilocks" >/dev/null 2>&1; then
        log_success "Goldilocks package import succeeded"
    else
        log_error "Unable to import 'goldilocks'. Did you run pip install -e .?"
        exit 1
    fi
}

check_required_packages() {
    log_step "CHECKING PYTHON DEPENDENCIES"
    local packages=("flask" "redis" "pymysql")
    for package in "${packages[@]}"; do
        check_python_package "$package"
    done
}

run_test_suite() {
    log_step "RUNNING PYTEST SUITE"
    run_command_test "Executing pytest" "$PROJECT_ROOT" "$PYTHON_BIN" -m pytest ${PYTEST_FLAGS}
}

run_type_checks() {
    log_step "RUNNING OPTIONAL TYPE CHECKS"
    if python_module_available "mypy"; then
        run_command_test "Executing mypy" "$PROJECT_ROOT" "$PYTHON_BIN" -m mypy .
    else
        log_warning "Skipping mypy check (module not installed)"
    fi
}

test_flask_endpoints() {
    log_step "TESTING FLASK ENDPOINTS"

    run_python_snippet "Validating /health endpoint" '\
from goldilocks.app import app

with app.test_client() as client:
    response = client.get("/health")
    if response.status_code != 200:
        raise SystemExit(f"Unexpected status code: {response.status_code}")

    payload = response.get_json()
    if not isinstance(payload, dict):
        raise SystemExit(f"Response is not JSON: {response.data!r}")

    status = payload.get("status")
    if status != "ok":
        raise SystemExit(f"Unexpected status value: {payload}")

    print(f"/health payload: {payload}")
'

    run_python_snippet "Validating /version endpoint" '\
from goldilocks.app import app

with app.test_client() as client:
    response = client.get("/version")
    if response.status_code != 200:
        raise SystemExit(f"Unexpected status code: {response.status_code}")

    payload = response.get_json()
    if not isinstance(payload, dict):
        raise SystemExit(f"Response is not JSON: {response.data!r}")

    expected_keys = {"app", "python", "flask"}
    missing = expected_keys - payload.keys()
    if missing:
        raise SystemExit(f"Missing keys from version payload: {missing}")

    print(f"/version payload: {payload}")
'
}

run_compiled_bytecode_check() {
    log_step "CHECKING PYTHON BYTECODE COMPILEABILITY"
    run_command_test "Compiling project modules" "$PROJECT_ROOT" "$PYTHON_BIN" -m compileall -q src
}

# Main test execution --------------------------------------------------------
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              GOLDILOCKS STACK TEST SUITE                     ║"
    echo "║                     LOCAL RELIABILITY MODE                   ║"
    echo "║                                                              ║"
    echo "║  Comprehensive validation of the local Python environment,   ║"
    echo "║  automated tests, and Flask endpoints without Docker.        ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""

    log_info "Project root: $PROJECT_ROOT"
    log_info "Python interpreter: $PYTHON_BIN"
    echo ""

    validate_environment
    check_required_packages
    run_test_suite
    run_type_checks
    run_compiled_bytecode_check
    test_flask_endpoints

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
        echo -e "${GREEN}║  The Goldilocks local environment is healthy and verified.  ║${NC}"
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
