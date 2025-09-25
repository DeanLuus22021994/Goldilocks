#!/bin/bash

# ==============================================================================
# GitHub Copilot Extension Provisioning Script for VS Code Server Insiders
# ==============================================================================
# This script ensures GitHub Copilot and GitHub Copilot Chat extensions are
# immediately available and enabled when VS Code Server Insiders starts
# ==============================================================================

set -euo pipefail

# Configuration
EXTENSIONS_DIR="/root/.vscode-server-insiders/extensions"
DATA_DIR="/root/.vscode-server-insiders/data"
LOGS_DIR="/root/.vscode-server-insiders/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[Copilot Provisioner]${NC} $1"
}

success() {
    echo -e "${GREEN}[Copilot Provisioner]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[Copilot Provisioner]${NC} $1"
}

error() {
    echo -e "${RED}[Copilot Provisioner]${NC} $1"
}

# Ensure directories exist
ensure_directories() {
    log "Ensuring VS Code Server directories exist..."

    mkdir -p "$EXTENSIONS_DIR"
    mkdir -p "$DATA_DIR"
    mkdir -p "$LOGS_DIR"

    # Set proper permissions
    chmod -R 755 "$EXTENSIONS_DIR"
    chmod -R 755 "$DATA_DIR"
    chmod -R 755 "$LOGS_DIR"

    success "Directories created and permissions set"
}

# Setup GitHub Copilot extensions configuration
setup_extensions_config() {
    log "Setting up GitHub Copilot extensions configuration..."

    # Ensure extensions.json exists and has the correct content
    if [[ ! -f "$EXTENSIONS_DIR/extensions.json" ]]; then
        cat > "$EXTENSIONS_DIR/extensions.json" << 'EOF'
{
  "recommendations": [
    "github.copilot",
    "github.copilot-chat"
  ],
  "unwantedRecommendations": []
}
EOF
        success "Created extensions.json with GitHub Copilot configuration"
    else
        success "extensions.json already exists"
    fi

    chmod 644 "$EXTENSIONS_DIR/extensions.json"
}

# Create extension manifest for immediate loading
create_extension_manifest() {
    log "Creating extension manifest for GitHub Copilot..."

    cat > "$EXTENSIONS_DIR/extensions-manifest.json" << 'EOF'
{
  "extensions": [
    {
      "id": "github.copilot",
      "preRelease": false,
      "enabled": true,
      "priority": "high"
    },
    {
      "id": "github.copilot-chat",
      "preRelease": false,
      "enabled": true,
      "priority": "high"
    }
  ],
  "autoInstall": true,
  "autoEnable": true
}
EOF

    chmod 644 "$EXTENSIONS_DIR/extensions-manifest.json"
    success "Extension manifest created"
}

# Setup user data directory with Copilot preferences
setup_user_data() {
    log "Setting up user data with GitHub Copilot preferences..."

    mkdir -p "$DATA_DIR/User"

    # Create settings.json with Copilot enabled
    cat > "$DATA_DIR/User/settings.json" << 'EOF'
{
    "github.copilot.enable": {
        "*": true,
        "yaml": true,
        "plaintext": true,
        "markdown": true,
        "python": true,
        "javascript": true,
        "typescript": true,
        "html": true,
        "css": true,
        "json": true,
        "jsonc": true,
        "dockerfile": true,
        "shellscript": true
    },
    "github.copilot.chat.enabled": true,
    "github.copilot.chat.welcomeMessage": "enabled",
    "github.copilot.renameSuggestions.triggerAutomatically": true,
    "github.copilot.editor.enableAutoCompletions": true,
    "github.copilot.editor.enableCodeActions": true,
    "github.copilot.inlineSuggest.enable": true,
    "github.copilot.inlineSuggest.count": 3,
    "extensions.autoCheckUpdates": false,
    "extensions.autoUpdate": false
}
EOF

    chmod 644 "$DATA_DIR/User/settings.json"
    success "User settings configured with GitHub Copilot preferences"
}

# Verify GitHub Copilot setup
verify_setup() {
    log "Verifying GitHub Copilot setup..."

    local errors=0

    if [[ ! -f "$EXTENSIONS_DIR/extensions.json" ]]; then
        error "extensions.json not found"
        ((errors++))
    fi

    if [[ ! -f "$EXTENSIONS_DIR/extensions-manifest.json" ]]; then
        error "extensions-manifest.json not found"
        ((errors++))
    fi

    if [[ ! -f "$DATA_DIR/User/settings.json" ]]; then
        error "User settings.json not found"
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        success "GitHub Copilot setup verification passed"
        return 0
    else
        error "GitHub Copilot setup verification failed with $errors errors"
        return 1
    fi
}

# Main execution
main() {
    log "Starting GitHub Copilot extension provisioning..."

    ensure_directories
    setup_extensions_config
    create_extension_manifest
    setup_user_data

    if verify_setup; then
        success "GitHub Copilot extension provisioning completed successfully!"
        success "Extensions will be available immediately when VS Code Server starts"
    else
        error "GitHub Copilot extension provisioning failed!"
        exit 1
    fi
}

# Run main function
main "$@"
