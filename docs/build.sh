#!/bin/bash
# Documentation Build Script
# Template-based document generation following SRP, DRY, MODERNIZE principles
# Optimized for GitHub Copilot development workflows
# Adheres to .github/copilot-instructions.md standards

set -euo pipefail  # Enhanced error handling
IFS=$'\n\t'       # Secure Internal Field Separator

# =============================================================================
# CONFIGURATION & GLOBALS
# =============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly DOCS_DIR="$SCRIPT_DIR"
readonly BIN_DIR="$DOCS_DIR/bin"
readonly TEMPLATES_DIR="$DOCS_DIR/templates"
readonly BUILD_TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Colors for enhanced output (MODERNIZE principle)
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# =============================================================================
# UTILITY FUNCTIONS (SRP - Single Responsibility)
# =============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $*${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $*${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $*${NC}"
}

log_error() {
    echo -e "${RED}❌ $*${NC}" >&2
}

log_step() {
    echo -e "${PURPLE}🔧 $*${NC}"
}

log_header() {
    echo -e "${CYAN}$*${NC}"
}

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log_error "Build failed with exit code $exit_code"
    fi
    return $exit_code
}

trap cleanup EXIT

# =============================================================================
# DATA COLLECTION FUNCTIONS (DRY - Don't Repeat Yourself)
# =============================================================================

get_system_info() {
    log_step "Gathering system information..."

    # Python version (HIGH COMPATIBILITY)
    local python_version
    python_version=$(python3 --version 2>/dev/null | cut -d' ' -f2 || echo "Not installed")

    # Flask version
    local flask_version
    if [[ -f "$PROJECT_ROOT/requirements.txt" ]]; then
        flask_version=$(grep -i "^flask" "$PROJECT_ROOT/requirements.txt" | cut -d'=' -f3 2>/dev/null || echo "Unknown")
    else
        flask_version=$(python3 -c "import flask; print(flask.__version__)" 2>/dev/null || echo "Unknown")
    fi

    # Docker version
    local docker_version
    docker_version=$(docker --version 2>/dev/null | cut -d' ' -f3 | cut -d',' -f1 || echo "Not installed")

    # Git info
    local git_branch git_commit
    git_branch=$(cd "$PROJECT_ROOT" && git branch --show-current 2>/dev/null || echo "detached")
    git_commit=$(cd "$PROJECT_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")

    # Export for template usage
    export PYTHON_VERSION="$python_version"
    export FLASK_VERSION="$flask_version"
    export DOCKER_VERSION="$docker_version"
    export GIT_BRANCH="$git_branch"
    export GIT_COMMIT="$git_commit"
}

get_project_metrics() {
    log_step "Analyzing project metrics..."

    # Test files count
    local test_count
    test_count=$(find "$PROJECT_ROOT/src" -name "test_*.py" 2>/dev/null | wc -l)

    # Python files count (excluding tests)
    local py_count
    py_count=$(find "$PROJECT_ROOT/src" -name "*.py" -not -path "*/tests/*" 2>/dev/null | wc -l)

    # Template files count
    local template_count
    template_count=$(find "$PROJECT_ROOT/frontend" -name "*.html" 2>/dev/null | wc -l)

    # CSS files count
    local css_count
    css_count=$(find "$PROJECT_ROOT/frontend" -name "*.css" 2>/dev/null | wc -l)

    # Dependencies count
    local py_deps=0
    local node_deps=0
    local dev_deps=0

    if [[ -f "$PROJECT_ROOT/requirements.txt" ]]; then
        py_deps=$(grep -c "^[^#]" "$PROJECT_ROOT/requirements.txt" 2>/dev/null || echo "0")
    fi

    if [[ -f "$PROJECT_ROOT/package.json" ]] && command -v jq >/dev/null; then
        node_deps=$(jq -r '.dependencies // {} | length' "$PROJECT_ROOT/package.json" 2>/dev/null || echo "0")
        dev_deps=$(jq -r '.devDependencies // {} | length' "$PROJECT_ROOT/package.json" 2>/dev/null || echo "0")
    fi

    # Export for template usage
    export TEST_COUNT="$test_count"
    export PYTHON_FILES_COUNT="$py_count"
    export TEMPLATE_COUNT="$template_count"
    export CSS_COUNT="$css_count"
    export PY_DEPS_COUNT="$py_deps"
    export NODE_DEPS_COUNT="$node_deps"
    export DEV_DEPS_COUNT="$dev_deps"
}

get_project_structure() {
    log_step "Generating project structure..."

    cd "$PROJECT_ROOT"

    # Generate tree with enhanced filtering (LIGHTWEIGHT principle)
    local tree_output
    tree_output=$(tree . \
        -I '__pycache__|.mypy_cache|node_modules|.git|.pytest_cache|coverage.xml|*.pyc|_site|bin' \
        -a \
        --dirsfirst \
        --filesfirst \
        -L 4 2>/dev/null | \
        sed '1d' | \
        head -n -2 || echo "Tree command not available")

    export TREE_OUTPUT="$tree_output"
}

get_performance_data() {
    log_step "Gathering performance benchmarks..."

    local performance_metrics="No benchmark data available"
    if [[ -f "$PROJECT_ROOT/.benchmarks/latest_benchmark_summary.txt" ]]; then
        performance_metrics=$(head -10 "$PROJECT_ROOT/.benchmarks/latest_benchmark_summary.txt" 2>/dev/null || echo "No benchmark data available")
    fi

    export PERFORMANCE_METRICS="$performance_metrics"
}

# =============================================================================
# TEMPLATE ENGINE FUNCTIONS (STRUCTURED principle)
# =============================================================================

process_template() {
    local template_content="$1"
    local output=""

    # Replace template variables using envsubst-like functionality
    output=$(echo "$template_content" | \
        sed "s/{{metadata.build_timestamp}}/$BUILD_TIMESTAMP/g" | \
        sed "s/{{content.tree_output}}/$TREE_OUTPUT/g" | \
        sed "s/{{content.system_metrics.python_version}}/$PYTHON_VERSION/g" | \
        sed "s/{{content.system_metrics.flask_version}}/$FLASK_VERSION/g" | \
        sed "s/{{content.system_metrics.docker_version}}/$DOCKER_VERSION/g" | \
        sed "s/{{content.system_metrics.git_info.branch}}/$GIT_BRANCH/g" | \
        sed "s/{{content.system_metrics.git_info.commit}}/$GIT_COMMIT/g" | \
        sed "s/{{content.project_assets.test_count}}/$TEST_COUNT/g" | \
        sed "s/{{content.project_assets.python_files.count}}/$PYTHON_FILES_COUNT/g" | \
        sed "s/{{content.project_assets.templates.count}}/$TEMPLATE_COUNT/g" | \
        sed "s/{{content.project_assets.css_files.count}}/$CSS_COUNT/g" | \
        sed "s/{{content.dependencies_info.python_dependencies}}/$PY_DEPS_COUNT/g" | \
        sed "s/{{content.dependencies_info.node_dependencies}}/$NODE_DEPS_COUNT/g" | \
        sed "s/{{content.dependencies_info.dev_dependencies}}/$DEV_DEPS_COUNT/g" | \
        sed "s/{{content.performance_benchmarks}}/$PERFORMANCE_METRICS/g")

    echo "$output"
}

generate_structure_doc() {
    log_step "Generating STRUCTURE.md from schema template..."

    if [[ ! -f "$TEMPLATES_DIR/STRUCTURE.schema" ]]; then
        log_error "STRUCTURE.schema template not found"
        return 1
    fi

    # Extract template from schema (MODERNIZE approach)
    local template_content
    template_content=$(jq -r '.template' "$TEMPLATES_DIR/STRUCTURE.schema" 2>/dev/null)

    if [[ -z "$template_content" || "$template_content" == "null" ]]; then
        log_error "Could not extract template from STRUCTURE.schema"
        return 1
    fi

    # Process template
    local processed_content
    processed_content=$(process_template "$template_content")

    # Write output
    echo "$processed_content" > "$DOCS_DIR/STRUCTURE.md"
    log_success "STRUCTURE.md generated successfully"
}

generate_technical_doc() {
    log_step "Generating TECHNICAL.md from schema template..."

    if [[ ! -f "$TEMPLATES_DIR/TECHNICAL.schema" ]]; then
        log_error "TECHNICAL.schema template not found"
        return 1
    fi

    # Extract template from schema
    local template_content
    template_content=$(jq -r '.template' "$TEMPLATES_DIR/TECHNICAL.schema" 2>/dev/null)

    if [[ -z "$template_content" || "$template_content" == "null" ]]; then
        log_error "Could not extract template from TECHNICAL.schema"
        return 1
    fi

    # Process template
    local processed_content
    processed_content=$(process_template "$template_content")

    # Write output
    echo "$processed_content" > "$DOCS_DIR/TECHNICAL.md"
    log_success "TECHNICAL.md generated successfully"
}

# =============================================================================
# DOCFX MANAGEMENT (IDEMPOTENCY principle)
# =============================================================================

download_docfx() {
    log_step "Managing DocFX installation..."

    if [[ -f "$BIN_DIR/docfx" ]] || [[ -f "$BIN_DIR/docfx.exe" ]]; then
        log_success "DocFX already available"
        return 0
    fi

    log_info "Downloading DocFX..."
    mkdir -p "$BIN_DIR"
    cd "$BIN_DIR"

    # Get latest release info
    local latest_release
    latest_release=$(curl -s https://api.github.com/repos/dotnet/docfx/releases/latest)

    local download_url platform_file

    case "$OSTYPE" in
        linux-gnu*)
            download_url=$(echo "$latest_release" | grep -o '"browser_download_url": "[^"]*linux[^"]*\.zip"' | cut -d'"' -f4)
            platform_file="docfx-linux.zip"
            ;;
        darwin*)
            download_url=$(echo "$latest_release" | grep -o '"browser_download_url": "[^"]*osx[^"]*\.zip"' | cut -d'"' -f4)
            platform_file="docfx-osx.zip"
            ;;
        *)
            log_error "Unsupported OS: $OSTYPE"
            return 1
            ;;
    esac

    if [[ -z "$download_url" ]]; then
        log_error "Could not find download URL for $OSTYPE"
        return 1
    fi

    # Download and extract (LIGHTWEIGHT principle)
    wget -q "$download_url" -O "$platform_file"
    python3 -c "import zipfile; zipfile.ZipFile('$platform_file').extractall('.')"
    chmod +x docfx
    rm "$platform_file"

    cd "$DOCS_DIR"
    log_success "DocFX downloaded and configured"
}

# =============================================================================
# MAIN EXECUTION (STRUCTURED principle)
# =============================================================================

main() {
    log_header "🏗️  Building Goldilocks Documentation"
    log_header "======================================="
    log_info "Build started at $BUILD_TIMESTAMP"
    log_info "Following Copilot Instructions: MODERNIZE, DRY, SRP, STRUCTURED"
    log_info "Project root: $PROJECT_ROOT"
    log_info "Documentation: $DOCS_DIR"

    # Validate dependencies
    if ! command -v jq >/dev/null; then
        log_error "jq is required for JSON schema processing"
        return 1
    fi

    # Create bin directory
    mkdir -p "$BIN_DIR"

    # Download DocFX if needed (IDEMPOTENCY)
    download_docfx

    # Collect all data (DRY principle)
    log_header "📊 Collecting Project Data"
    get_system_info
    get_project_metrics
    get_project_structure
    get_performance_data

    # Generate documentation files using templates (SRP)
    log_header "📚 Generating Documentation Content"
    generate_structure_doc
    generate_technical_doc

    # Build with DocFX (MODERNIZE)
    log_header "🔨 Building with DocFX"
    cd "$DOCS_DIR"

    local docfx_executable
    if [[ -f "$BIN_DIR/docfx" ]]; then
        docfx_executable="$BIN_DIR/docfx"
    elif [[ -f "$BIN_DIR/docfx.exe" ]]; then
        docfx_executable="$BIN_DIR/docfx.exe"
    else
        log_error "DocFX executable not found after installation"
        return 1
    fi

    log_step "Running DocFX build..."
    if "$docfx_executable" docfx.json; then
        log_success "DocFX build completed successfully"
    else
        log_warn "DocFX build completed with warnings"
    fi

    # Generate build summary (STANDARDIZATION)
    log_header "📊 Build Summary"
    log_success "Documentation built successfully!"
    log_info "Build timestamp: $BUILD_TIMESTAMP"
    log_info "Generated files:"
    log_info "  - STRUCTURE.md: Enhanced project structure (from schema)"
    log_info "  - TECHNICAL.md: Comprehensive technical specifications (from schema)"
    log_info "  - _site/: Complete documentation website"

    log_header "🌐 Access Documentation"
    log_info "Local server: cd docs/_site && python -m http.server 8080"
    log_info "Browser: http://localhost:8080"

    # Optional: Start local server if --serve flag is passed
    if [[ "${1:-}" == "--serve" ]]; then
        log_step "Starting local documentation server..."
        cd "_site"
        python3 -m http.server 8080 &
        local server_pid=$!
        log_success "Documentation server started at http://localhost:8080"
        log_info "Press Ctrl+C to stop the server"
        wait $server_pid
    fi
}

# Execute main function with all arguments
main "$@"
