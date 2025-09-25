# GitHub Copilot Extensions Provisioning for Goldilocks DevContainer

## Overview

This setup is specifically focused on ensuring **GitHub Copilot** and **GitHub Copilot Chat** extensions are immediately available and fully functional when the DevContainer is built, eliminating the need to manually reload the window or wait for extension installation.

## Core Focus: GitHub Copilot Only

### Extensions Included

- `github.copilot` - AI pair programming
- `github.copilot-chat` - AI-powered chat conversations

### Key Features

- **Immediate Availability**: Extensions are pre-provisioned during container build
- **No Window Reloads**: Extensions load instantly when VS Code connects
- **Persistent Configuration**: Settings and data persist across container rebuilds
- **Optimized Performance**: Minimal overhead, focused solely on Copilot functionality

## Architecture

### Files Structure

```
.vscode-server-insiders/
└── extensions/
    └── extensions.json         # Extension recommendations and configuration
```

### Docker Integration

1. **Volume Persistence**: The VS Code Server extensions and data are persisted using Docker named volumes
2. **Automatic Setup**: Extensions are pre-configured during container build
3. **No Manual Intervention**: Extensions load automatically without requiring window reloads

## Configuration Details

### Extensions Included

#### Core GitHub Copilot Extensions

- `github.copilot` - AI pair programming
- `github.copilot-chat` - AI-powered chat conversations

#### Python Development Stack

- `ms-python.python` - Python language support
- `ms-python.vscode-pylance` - Advanced Python IntelliSense
- `charliermarsh.ruff` - Modern Python linting and formatting
- `ms-python.flake8` - Additional Python linting
- `ms-python.mypy-type-checker` - Type checking
- `ms-python.black-formatter` - Python code formatting
- `ms-python.isort` - Import organization

#### Language Support

- `redhat.vscode-yaml` - YAML language support
- `ms-vscode.vscode-json` - JSON language support

### Docker Volume Configuration

The following volumes are configured in `infrastructure/docker/compose/shared/volumes.yml`:

```yaml
goldilocks-vscode-server-extensions:
  name: goldilocks_vscode_server_extensions
  driver: local
  labels:
    com.goldilocks.volume.type: "development-tools"
    com.goldilocks.volume.purpose: "vscode-server-extensions"

goldilocks-vscode-server-data:
  name: goldilocks_vscode_server_data
  driver: local
  labels:
    com.goldilocks.volume.type: "development-tools"
    com.goldilocks.volume.purpose: "vscode-server-data"
```

### Backend Service Mounts

The backend service (`compose/services/backend.yml`) mounts these volumes:

```yaml
volumes:
  # VS Code Server extensions and data persistence
  - goldilocks-vscode-server-extensions:/root/.vscode-server-insiders/extensions
  - goldilocks-vscode-server-data:/root/.vscode-server-insiders/data
```

### Dockerfile Integration

The multi-stage Dockerfile creates the necessary directories and copies the extensions configuration:

```dockerfile
# Create VS Code Server directories
RUN mkdir -p /root/.vscode-server-insiders/extensions \
  /root/.vscode-server-insiders/data \
  /root/.vscode-server-insiders/logs

# Copy extensions configuration
COPY --chown=root:root .vscode-server-insiders/extensions/extensions.json /root/.vscode-server-insiders/extensions/extensions.json
```

## Usage

### First-Time Setup

1. The extensions.json file is automatically included in the container build
2. VS Code Server volumes persist extensions and data across rebuilds
3. Extensions are automatically available on container start

### Container Rebuild

1. Run: `docker-compose down && docker-compose --profile dev up -d --build`
2. Open VS Code - extensions should be immediately available
3. No window reload required

### Verification

You can verify the setup by checking:

1. Extensions are visible in the Extensions panel
2. GitHub Copilot is enabled and functional
3. Python development tools are active

## Benefits

1. **Seamless Experience**: No manual extension installation or window reloads
2. **Consistent Environment**: All team members get the same extension configuration
3. **Fast Startup**: Extensions are pre-installed and cached
4. **Infrastructure Integration**: Fully integrated with the Docker-based development environment

## Troubleshooting

### Extensions Not Loading

1. Verify the volumes are properly mounted: `docker inspect goldilocks-backend`
2. Check if extensions.json exists in container: `docker exec goldilocks-backend ls -la /root/.vscode-server-insiders/extensions/`
3. Review container logs for VS Code Server startup messages

### Extension Conflicts

The `unwantedRecommendations` array prevents conflicting extensions (like pylint when using ruff)

### Performance Issues

VS Code Server extensions and data use persistent Docker volumes optimized for development performance

## Maintenance

### Adding New Extensions

1. Add extension ID to the `recommendations` array in `extensions.json`
2. Rebuild the container to apply changes
3. Extensions will be available immediately on next connection

### Removing Extensions

1. Add extension ID to the `unwantedRecommendations` array
2. Remove from `recommendations` array if present
3. Rebuild the container
