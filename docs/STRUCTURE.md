# Project Structure

Generated on: 2025-09-25 13:08:31

## Overview

This document provides a comprehensive overview of the Goldilocks project
structure, following modern development practices and clean architecture
principles.

## Project Metrics

- **Total Files**: 2182
- **Lines of Code**: 6,549
- **Test Files**: 16
- **Docker Files**: 5
- **GitHub Actions**: 2

## Directory Structure

```
/projects/Goldilocks
├── AGENT.md
├── Dockerfile
├── Makefile
├── README.md
├── app.py
├── clean.py
├── config
│   ├── cypress.config.js
│   ├── globals.xml
│   └── pyproject.toml
├── coverage.xml
├── cypress
│   ├── e2e
│   │   └── smoke.cy.js
│   └── support
│       └── e2e.js
├── docker-bake.json
├── docs
│   ├── DOCKER.md
│   ├── README.md
│   ├── STRUCTURE.md
│   ├── TECHNICAL.md
│   └── generate.py
├── frontend
│   └── static
│       ├── css
│       │   ├── base.css
│       │   ├── buttons.css
│       │   ├── components.css
│       │   ├── footer.css
│       │   ├── header.css
│       │   ├── layout.css
│       │   ├── nav.css
│       │   ├── theme.css
│       │   ├── utilities.css
│       │   └── variables.css
│       ├── favicon.svg
│       ├── index.html
│       ├── js
│       │   └── main.js
│       └── templates
│           ├── auth
│           │   ├── dashboard.html
│           │   ├── login.html
│           │   ├── profile.html
│           │   └── register.html
│           ├── components
│           │   ├── alert.html
│           │   ├── breadcrumb.html
│           │   ├── card.html
│           │   ├── form-input.html
│           │   ├── loading.html
│           │   └── modal.html
│           ├── dialog
│           │   ├── alert.html
│           │   ├── confirm.html
│           │   ├── form.html
│           │   ├── loading.html
│           │   └── prompt.html
│           ├── errors
│           │   ├── 400.html
│           │   ├── 403.html
│           │   ├── 404.html
│           │   ├── 500.html
│           │   └── maintenance.html
│           ├── layouts
│           │   ├── admin.html
│           │   ├── base.html
│           │   ├── clean.html
│           │   ├── single-column.html
│           │   └── two-column.html
│           └── main
│               └── index.html
├── infrastructure
│   └── docker
│       ├── compose
│       │   ├── overrides
│       │   │   ├── ci-cd.yml
│       │   │   ├── development.yml
│       │   │   ├── edge.yml
│       │   │   ├── production.yml
│       │   │   └── testing.yml
│       │   ├── services
│       │   │   ├── adminer.yml
│       │   │   ├── backend.yml
│       │   │   ├── database.yml
│       │   │   └── frontend.yml
│       │   └── shared
│       │       ├── environment.env
│       │       ├── networks.yml
│       │       ├── secrets.yml
│       │       └── volumes.yml
│       ├── database-init
│       │   └── 01-init-database.sql
│       ├── docker-compose.yml
│       ├── dockerfiles
│       │   ├── Dockerfile.development
│       │   ├── Dockerfile.multi-stage
│       │   └── Dockerfile.production
│       └── scripts
│           ├── compose.sh
│           ├── entrypoints
│           │   ├── entrypoint-dev.sh
│           │   └── entrypoint-prod.sh
│           └── test-infrastructure.sh
├── package-lock.json
├── package.json
├── pyproject.toml
├── requirements.txt
├── scripts
│   ├── compile-bytecode.ps1
│   └── compile-bytecode.sh
├── src
│   ├── docs
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── collectors.py
│   │   ├── generators.py
│   │   ├── models.py
│   │   ├── processors.py
│   │   └── service.py
│   ├── goldilocks
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── main.py
│   │   ├── app.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   └── app_factory.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── forms.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   └── utils
│   │       └── __init__.py
│   ├── instance
│   │   └── goldilocks.db
│   ├── pyproject.toml
│   ├── setup.py
│   └── tests
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── test_api_endpoints.py
│       │   └── test_auth_endpoints.py
│       ├── conftest.py
│       ├── core
│       │   ├── __init__.py
│       │   └── test_app_factory.py
│       ├── docs
│       │   ├── __init__.py
│       │   ├── test_collectors.py
│       │   ├── test_generators.py
│       │   └── test_service.py
│       ├── errors
│       │   ├── __init__.py
│       │   └── test_404.py
│       ├── health
│       │   ├── __init__.py
│       │   └── test_health.py
│       ├── index
│       │   ├── test_index.py
│       │   └── version
│       ├── models
│       │   ├── __init__.py
│       │   └── test_database_models.py
│       ├── services
│       │   ├── __init__.py
│       │   └── test_auth_service.py
│       ├── templates
│       │   ├── __init__.py
│       │   └── test_template_system.py
│       ├── utils
│       │   ├── __init__.py
│       │   ├── test_helpers.py
│       │   └── test_utils.py
│       └── version
│           ├── __init__.py
│           ├── test_version.py
│           └── test_version_fallback.py
└── start-dev.sh

50 directories, 137 files

```

## Architecture Principles

The project follows these key principles from
`.github/copilot-instructions.md`:

- **SEPARATION OF CONCERNS**: Each module handles only its specific
  responsibility
- **NO CROSS-CUTTING CONCERNS**: Avoid functionality that spans multiple
  modules
- **DRY**: Don't Repeat Yourself - abstract common patterns
- **SRP**: Single Responsibility Principle - one purpose per
  function/class
- **SOLID**: Follow all SOLID principles for clean, maintainable
  design

## Key Directories

### `/src/goldilocks/`
Core application source code following modular architecture.

### `/tests/`
Comprehensive test suite with 100% coverage target.

### `/docs/`
Documentation generated using modern tooling and markitdown integration.

### `/infrastructure/`
Docker configurations and deployment resources.

### `/frontend/`
Static assets and frontend components.

### `/scripts/`
Utility scripts for development and deployment.

## Development Workflow

The project uses modern development practices:
- Pre-commit hooks for code quality
- CI/CD validation via GitHub Actions
- Docker-based development environment
- VS Code integration with MCP servers

## Generated Documentation

This document is automatically generated using modern Python tooling
and the markitdown package for enhanced markdown processing.
