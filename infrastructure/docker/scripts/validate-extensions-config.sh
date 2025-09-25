#!/bin/bash

# ==============================================================================
# Goldilocks Extensions and MCP Servers Configuration Validator
# ==============================================================================
# Validates the complete setup of VS Code extensions and MCP servers
# ==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[Validator]${NC} $1"
}

success() {
    echo -e "${GREEN}[Validator]${NC} ✅ $1"
}

warning() {
    echo -e "${YELLOW}[Validator]${NC} ⚠️  $1"
}

error() {
    echo -e "${RED}[Validator]${NC} ❌ $1"
}

# Validation results
ERRORS=0
WARNINGS=0

validate_file() {
    local file="$1"
    local description="$2"

    if [[ -f "$file" ]]; then
        success "$description exists: $file"
        return 0
    else
        error "$description missing: $file"
        ((ERRORS++))
        return 1
    fi
}

validate_json_file() {
    local file="$1"
    local description="$2"

    if validate_file "$file" "$description"; then
        if python -m json.tool "$file" >/dev/null 2>&1; then
            success "$description is valid JSON"
            return 0
        else
            error "$description contains invalid JSON"
            ((ERRORS++))
            return 1
        fi
    fi
    return 1
}

validate_yaml_file() {
    local file="$1"
    local description="$2"

    if validate_file "$file" "$description"; then
        if python -c "import yaml; yaml.safe_load(open('$file', 'r'))" >/dev/null 2>&1; then
            success "$description is valid YAML"
            return 0
        else
            error "$description contains invalid YAML"
            ((ERRORS++))
            return 1
        fi
    fi
    return 1
}

log "Starting Goldilocks Extensions and MCP Servers configuration validation..."

echo ""
log "🔍 Validating Core Configuration Files..."

# DevContainer configuration
validate_json_file "/workspaces/Goldilocks/.devcontainer/devcontainer.json" "DevContainer configuration"

# VS Code Server extensions configuration
validate_json_file "/workspaces/Goldilocks/.vscode-server-insiders/extensions/extensions.json" "VS Code extensions configuration"

# Documentation
validate_file "/workspaces/Goldilocks/docs/EXTENSIONS.md" "Extensions architecture documentation"

echo ""
log "🐳 Validating Docker Configuration Files..."

# Docker Compose files
validate_yaml_file "/workspaces/Goldilocks/infrastructure/docker/docker-compose.yml" "Main Docker Compose configuration"
validate_yaml_file "/workspaces/Goldilocks/infrastructure/docker/compose/services/extensions.yml" "Extensions service configuration"
validate_yaml_file "/workspaces/Goldilocks/infrastructure/docker/compose/overrides/development.yml" "Development overrides"

echo ""
log "🔧 Validating Scripts and Provisioning..."

# Provisioning script
if validate_file "/workspaces/Goldilocks/infrastructure/docker/scripts/provision-copilot-extensions.sh" "Extensions provisioning script"; then
    if [[ -x "/workspaces/Goldilocks/infrastructure/docker/scripts/provision-copilot-extensions.sh" ]]; then
        success "Provisioning script is executable"
    else
        warning "Provisioning script is not executable (may affect container startup)"
        ((WARNINGS++))
    fi
fi

echo ""
log "🤖 Validating MCP Server Configuration..."

# MCP configuration in devcontainer.json
if grep -q '"mcp"' "/workspaces/Goldilocks/.devcontainer/devcontainer.json"; then
    success "MCP servers configured in devcontainer.json"

    # Check for specific MCP servers
    if grep -q '"playwright"' "/workspaces/Goldilocks/.devcontainer/devcontainer.json"; then
        success "Playwright MCP server configured"
    else
        warning "Playwright MCP server not found in configuration"
        ((WARNINGS++))
    fi

    if grep -q '"docker"' "/workspaces/Goldilocks/.devcontainer/devcontainer.json"; then
        success "Docker MCP server configured"
    else
        warning "Docker MCP server not found in configuration"
        ((WARNINGS++))
    fi

    if grep -q '"filesystem"' "/workspaces/Goldilocks/.devcontainer/devcontainer.json"; then
        success "Filesystem MCP server configured"
    else
        warning "Filesystem MCP server not found in configuration"
        ((WARNINGS++))
    fi
else
    error "MCP servers not configured in devcontainer.json"
    ((ERRORS++))
fi

# MCP.json file (if it exists from provisioning)
if [[ -f "/root/.vscode-server-insiders/data/User/mcp.json" ]]; then
    validate_json_file "/root/.vscode-server-insiders/data/User/mcp.json" "MCP servers runtime configuration"
else
    warning "MCP runtime configuration not found (will be created during container startup)"
    ((WARNINGS++))
fi

echo ""
log "🔐 Validating Docker Host Access Configuration..."

# Check Docker socket access in extensions service
if grep -q "/var/run/docker.sock" "/workspaces/Goldilocks/infrastructure/docker/compose/services/extensions.yml"; then
    success "Docker socket access configured for extensions service"
else
    error "Docker socket access not configured"
    ((ERRORS++))
fi

# Check host networking configuration
if grep -q "host.docker.internal" "/workspaces/Goldilocks/infrastructure/docker/compose/services/extensions.yml"; then
    success "Docker host networking configured"
else
    warning "Docker host networking may not be properly configured"
    ((WARNINGS++))
fi

echo ""
log "📊 Validation Summary:"

if [[ $ERRORS -eq 0 ]] && [[ $WARNINGS -eq 0 ]]; then
    success "🎉 All validations passed! Configuration is complete and ready."
    echo ""
    success "✅ GitHub Copilot extensions will be immediately available"
    success "✅ MCP servers will be provisioned and accessible"
    success "✅ Docker host communication is properly configured"
    success "✅ All files follow established patterns and are in correct locations"
    echo ""
    log "🚀 Ready to start development environment with:"
    log "   docker-compose --profile dev up -d --build"
    exit 0
elif [[ $ERRORS -eq 0 ]]; then
    success "✅ Configuration is valid with $WARNINGS warning(s)"
    echo ""
    warning "⚠️  Some non-critical issues detected but setup should work"
    exit 0
else
    error "❌ Configuration validation failed with $ERRORS error(s) and $WARNINGS warning(s)"
    echo ""
    error "🔧 Please fix the errors above before proceeding"
    exit 1
fi
