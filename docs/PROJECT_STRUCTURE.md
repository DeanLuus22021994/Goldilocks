---
uid: goldilocks.structure
title: Project Structure
description: File organization, module descriptions, and dependency mapping for Goldilocks
author: Goldilocks Development Team
ms.date: 2024-09-24
---

# Project Structure

This document explains the organized project structure and where to find different types of files.

> [!NOTE]
> This structure is automatically validated by DocFX to ensure documentation stays current with the codebase.

## Directory Structure

```text
├── config/          # Configuration files for tools and frameworks
│   ├── pyproject.toml        # Python project configuration
│   ├── cypress.config.js     # Cypress E2E test configuration
│   └── .pre-commit-config.yaml # Pre-commit hooks configuration
├── docs/            # Documentation files
│   ├── README.md            # Main project documentation
│   └── TECHNICAL_SPECIFICATIONS.md
├── infrastructure/  # Container and deployment configurations
│   ├── docker/              # Docker multi-stage builds
│   └── kubernetes/          # K8s manifests (future)
├── scripts/         # Build and automation scripts
│   ├── compile-bytecode.ps1 # Python bytecode compilation
│   └── compile-bytecode.sh  # Linux version
├── src/            # Source code
│   └── goldilocks/         # Main Python package
├── frontend/       # Frontend static assets
│   └── static/            # CSS, JS, HTML files
└── tests/          # Legacy test location (moved to src/goldilocks/tests/)
```

## File Organization Principles

### Configuration Files (`config/`)

- All tool configurations are centralized here
- Original files are kept in config/, with copies in root only when required by tools
- Examples: pytest, mypy, flake8, cypress, pre-commit

### Documentation (`docs/`)

- All project documentation
- README.md is copied to root for GitHub compatibility
- Technical specifications and development guides

### Infrastructure (`infrastructure/`)

- Container definitions (multi-stage Dockerfiles)
- Deployment configurations
- Environment-specific setups

### Scripts (`scripts/`)

- Build automation scripts
- Development utilities
- Cross-platform (bash + PowerShell versions)

### Source Code (`src/`)

- All Python source code in `src/goldilocks/`
- Tests are in `src/goldilocks/tests/`
- Follows Python src layout best practices

## Quick Start

1. **Development**: Use the optimized devcontainer or Docker compose
2. **Testing**: `python -m pytest` (uses config/pyproject.toml)
3. **E2E Tests**: `npm run test:e2e` (uses config/cypress.config.js)
4. **Build**: Use scripts in `scripts/` directory
5. **Deploy**: Use configurations in `infrastructure/`

For detailed information, see [docs/README.md](docs/README.md).
