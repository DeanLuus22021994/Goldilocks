# Extensions and MCP Servers Architecture - Development Tools Infrastructure

## Overview

Following the **SEPARATION OF CONCERNS** and **NO CROSS-CUTTING CONCERNS** principles from the Goldilocks Copilot instructions, the VS Code extensions provisioning and MCP (Model Context Protocol) servers have been refactored from cross-cutting concerns into dedicated, focused development tools infrastructure.

## Architecture Refactoring

### Before: Cross-Cutting Concerns ❌

```yaml
# backend.yml (VIOLATION of separation of concerns)
services:
  goldilocks-backend:
    volumes:
      - goldilocks-vscode-server-extensions:/root/.vscode-server-insiders/extensions
      - goldilocks-vscode-server-data:/root/.vscode-server-insiders/data
    environment:
      VSCODE_EXTENSIONS: /root/.vscode-server-insiders/extensions
      GITHUB_COPILOT_ENABLED: true
```

### After: Proper Separation of Concerns ✅

```yaml
# extensions.yml (DEDICATED service with single responsibility)
services:
  goldilocks-extensions:
    # Single Responsibility: VS Code extensions and MCP servers provisioning
    command: provision-copilot-extensions.sh
    volumes:
      - goldilocks-vscode-server-extensions:/root/.vscode-server-insiders/extensions
      - goldilocks-vscode-server-data:/root/.vscode-server-insiders/data
    # Docker host communication for infrastructure access
    network_mode: "host"

# backend.yml (CLEAN separation - only consumes provisioned extensions)
services:
  goldilocks-backend:
    volumes:
      - goldilocks-vscode-server-extensions:/root/.vscode-server-insiders/extensions:ro
    depends_on:
      goldilocks-extensions:
        condition: service_healthy
```

## Development Tools Infrastructure

### 🔧 Extensions Service (`compose/services/extensions.yml`)

**Single Responsibility**: VS Code extensions and MCP servers provisioning

- **Purpose**: Provision GitHub Copilot extensions and MCP servers during container startup
- **Scope**: VS Code Server extensions configuration and MCP server management
- **Lifecycle**: Runs once to provision, then remains idle
- **Resources**: Minimal (256M memory, 0.5 CPU)
- **Network**: Docker host communication enabled for infrastructure access

### 🤖 MCP Servers Integration

**Model Context Protocol servers** are provisioned alongside VS Code extensions:

- **Playwright MCP Server**: Web automation and testing
- **Docker Host Access**: Full communication with host for infrastructure management
- **Auto-Provisioning**: MCP servers installed during container build
- **DevContainer Integration**: Configured through `customizations.vscode.mcp` section

### 🚀 Backend Service (`compose/services/backend.yml`)

**Single Responsibility**: Application backend execution

- **Purpose**: Run the Flask application backend
- **Scope**: Application logic, API endpoints, business functionality
- **Lifecycle**: Long-running web server
- **Resources**: Full allocation (2G memory, 2.0 CPU)
- **Network**: Port 9000 exposed for application access

## MCP Servers Configuration

### DevContainer Configuration

```jsonc
{
  "dockerComposeFile": "../infrastructure/docker/docker-compose.yml",
  "service": "goldilocks-backend",
  "customizations": {
    "vscode": {
      "extensions": ["github.copilot", "github.copilot-chat"],
      "mcp": {
        "servers": {
          "playwright": {
            "command": "npx",
            "args": ["-y", "@microsoft/mcp-server-playwright"]
          },
          "docker": {
            "command": "docker",
            "args": ["--help"]
          }
        }
      }
    }
  }
}
```

### MCP Servers Provisioning Script

The extensions service provisions MCP servers through an enhanced script:

```bash
#!/bin/bash
# provision-copilot-extensions.sh

# Install Node.js and npm for MCP servers
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt-get install -y nodejs

# Install MCP servers
npm install -g @microsoft/mcp-server-playwright

# Configure MCP servers in VS Code
mkdir -p /root/.vscode-server-insiders/data/User
cat > /root/.vscode-server-insiders/data/User/mcp.json << 'EOF'
{
  "servers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@microsoft/mcp-server-playwright"]
    }
  }
}
EOF
```

## Docker Host Communication

### Network Configuration

For infrastructure access, the extensions service requires Docker host communication:

```yaml
# extensions.yml
services:
  goldilocks-extensions:
    # Enable full Docker host communication
    network_mode: "host"
    # OR alternative: bridge with host networking
    extra_hosts:
      - "host.docker.internal:host-gateway"
    # Docker socket access for infrastructure management
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Security Considerations

- Docker host access limited to extensions service only
- Backend service maintains network isolation
- Read-only Docker socket access for monitoring
- Host networking only for development environment

## Architectural Benefits

### ✅ Separation of Concerns

- **Backend Service**: Focused solely on application logic
- **Extensions Service**: Focused on development tools (VS Code + MCP servers)
- **Clear Boundaries**: No functionality bleeding between services

### ✅ Single Responsibility Principle (SRP)

- Each service has exactly one reason to change
- Extensions service changes only when development tools change
- Backend service changes only when application logic changes

### ✅ Infrastructure Integration

- **Docker Host Access**: Extensions service can manage infrastructure
- **MCP Servers**: Integrated with VS Code for enhanced development experience
- **Auto-Provisioning**: All development tools ready on container start

### ✅ High Cohesion

- All development tools functionality grouped in extensions service
- All application-related functionality remains in backend service
- MCP servers and VS Code extensions managed together

## Service Orchestration

### Dependency Management

```yaml
# Backend depends on extensions being provisioned
goldilocks-backend:
  depends_on:
    goldilocks-extensions:
      condition: service_healthy
      restart: false # Extensions provision once
```

### Volume Sharing

```yaml
# Extensions service provisions (read-write)
goldilocks-extensions:
  volumes:
    - goldilocks-vscode-server-extensions:/root/.vscode-server-insiders/extensions
    - goldilocks-vscode-server-data:/root/.vscode-server-insiders/data
    - /var/run/docker.sock:/var/run/docker.sock:ro # Docker host access

# Backend service consumes (read-only)
goldilocks-backend:
  volumes:
    - goldilocks-vscode-server-extensions:/root/.vscode-server-insiders/extensions:ro
    - goldilocks-vscode-server-data:/root/.vscode-server-insiders/data
```

## Environment-Specific Configuration

### Development Overrides (`compose/overrides/development.yml`)

```yaml
services:
  goldilocks-extensions:
    network_mode: "host" # Full host access for development
    environment:
      - EXTENSIONS_DEVELOPMENT_MODE=true
      - MCP_SERVERS_ENABLED=true
      - DOCKER_HOST_ACCESS=true
      - PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright-browsers
```

## File Structure

```
docs/
└── EXTENSIONS.md                    # This file - development tools architecture

infrastructure/docker/
├── scripts/
│   └── provision-copilot-extensions.sh  # Enhanced with MCP server support
└── compose/
    ├── services/
    │   ├── backend.yml              # Application backend (clean, focused)
    │   └── extensions.yml           # Development tools (VS Code + MCP servers)
    └── overrides/
        └── development.yml          # Extensions + MCP development configuration

.devcontainer/
└── devcontainer.json               # Enhanced with MCP server configuration
```

## Usage

### Start Extensions Service Only

```bash
docker-compose --profile extensions up -d goldilocks-extensions
```

### Start Development Environment (includes extensions + MCP servers)

```bash
docker-compose --profile dev up -d
```

### Verify Extensions and MCP Servers Provisioning

```bash
# Check extensions
docker-compose logs goldilocks-extensions
docker exec goldilocks-extensions ls -la /root/.vscode-server-insiders/extensions/

# Check MCP servers
docker exec goldilocks-extensions npx @microsoft/mcp-server-playwright --version
docker exec goldilocks-extensions cat /root/.vscode-server-insiders/data/User/mcp.json
```

## Compliance with Goldilocks Principles

- ✅ **SEPARATION OF CONCERNS**: Extensions and MCP servers isolated from application logic
- ✅ **NO CROSS-CUTTING**: No functionality spans multiple service concerns
- ✅ **STRUCTURED**: Follows established service pattern in `compose/services/`
- ✅ **DRY**: Reuses common Docker patterns and volume definitions
- ✅ **LIGHTWEIGHT**: Extensions service uses minimal resources
- ✅ **STANDARDIZATION**: Consistent with other service definitions
- ✅ **HIGH COMPATIBILITY**: Support for multiple environments and MCP server types
- ✅ **MODERNIZE**: Uses latest VS Code and MCP server technologies

## MCP Server Types Supported

### Available MCP Servers

- **@microsoft/mcp-server-playwright**: Web automation and testing
- **@microsoft/mcp-server-docker**: Docker container management
- **@microsoft/mcp-server-git**: Git repository operations
- **@microsoft/mcp-server-filesystem**: File system operations

### Custom MCP Server Integration

```bash
# Add custom MCP servers to provisioning script
npm install -g your-custom-mcp-server

# Update mcp.json configuration
{
  "servers": {
    "custom": {
      "command": "your-custom-mcp-server",
      "args": ["--config", "/path/to/config"]
    }
  }
}
```

This architecture transforms cross-cutting development tool concerns into a well-architected, focused service that maintains clean boundaries while providing comprehensive VS Code extensions and MCP server functionality with full Docker infrastructure access.
