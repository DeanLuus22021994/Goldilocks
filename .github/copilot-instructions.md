# Copilot Instructions for Goldilocks

## Core Development Principles

**MODERNIZE** - Use latest stable versions, current best practices, modern tooling
**DRY** - Don't Repeat Yourself, abstract common patterns, reuse code
**SRP** - Single Responsibility Principle, one purpose per function/class
**STRUCTURED** - Organized, predictable, maintainable codebase architecture
**MONOLITHIC** - Unified, cohesive application design avoiding unnecessary microservice complexity
**STANDARDIZATION** - Consistent coding style, patterns, and conventions throughout
**IDEMPOTENCY** - Operations produce same result when run multiple times
**SOLID** - Follow all SOLID principles for clean, maintainable object-oriented design
**LOW CODE** - Minimize boilerplate, leverage frameworks and tools effectively
**HIGH COMPATIBILITY** - Support multiple environments, Python versions, deployment targets
**LIGHTWEIGHT** - Efficient resource usage, minimal dependencies, fast startup
**LOW FOOTPRINT** - Small image sizes, memory-efficient, optimized for containers
**SEPARATION OF CONCERNS** - Clear separation between modules, avoid cross-cutting concerns
**NO CROSS-CUTTING** - Each module handles its own responsibilities without bleeding into others

## Repository Standards

### Architecture & Design Principles

- **SEPARATION OF CONCERNS** - Each module/function should handle only its specific responsibility
- **NO CROSS-CUTTING CONCERNS** - Avoid functionality that spans multiple modules or layers
- **CLEAN INTERFACES** - Well-defined boundaries between components
- **LOOSE COUPLING** - Minimize dependencies between modules
- **HIGH COHESION** - Keep related functionality together within modules

### Code Quality

- **100% test coverage** - All code paths must be tested
- **Type hints** - Use Python type annotations for all functions and methods
- **Linting compliance** - Zero flake8, mypy, black, isort violations
- **Documentation** - Docstrings for all public functions, clear README

### Development Workflow

- **Pre-commit hooks** - Automated formatting and linting before commits
- **CI/CD validation** - All tests, linting, type checking must pass
- **Branch protection** - No direct commits to main, require PR reviews
- **Semantic commits** - Clear, descriptive commit messages

### Performance & Efficiency

- **Minimal dependencies** - Only include necessary packages
- **Optimized Docker** - Multi-stage builds, minimal base images, layer caching
- **Resource efficiency** - Monitor memory usage, startup time, response times
- **Caching strategies** - Leverage pip cache, Docker layer cache, application caching

### Security Best Practices

- **No secrets in code** - Use environment variables and secret management
- **Dependency scanning** - Regular updates via Dependabot
- **Container security** - Non-root users, minimal attack surface
- **Input validation** - Sanitize and validate all user inputs

## Development Tips & Tricks

### VS Code Integration

- Use Dev Container for consistent environment
- Configure tasks for common operations (test, lint, run)
- Install recommended extensions (Python, Copilot, Docker)
- Use launch.json for debugging configurations

### Testing Strategy

- **Unit tests** - Test individual functions and methods
- **Integration tests** - Test API endpoints and workflows
- **Coverage reporting** - Use pytest-cov for coverage analysis
- **Test automation** - Run tests on every commit via CI/CD

### Docker Optimization

- Use Python slim images for smaller size
- Install system dependencies in one RUN command
- Copy requirements.txt first for better layer caching
- Use .dockerignore to exclude unnecessary files
- Set appropriate worker/thread configuration for gunicorn

### Local Development

- Use `make` commands for common tasks
- Leverage hot reload for development (Flask debug mode)
- Use `pytest -f` for test-driven development
- Configure pre-commit hooks for automatic formatting

### Monitoring & Observability

- Structured JSON logging for production
- Request correlation IDs for tracing
- Health check endpoints for monitoring
- Performance metrics and timing headers

### Documentation Standards

- **README first** - Clear setup and usage instructions
- **API documentation** - Document all endpoints and responses
- **Architecture decisions** - Record important technical decisions
- **Troubleshooting guides** - Common issues and solutions

## Copilot Usage Guidelines

### Code Generation

- Request minimal, focused changes
- Ask for type hints and docstrings
- Ensure generated code follows project conventions
- Validate generated tests cover edge cases

### Refactoring

- Focus on one principle at a time (DRY, SRP, etc.)
- Maintain backward compatibility
- Update tests after refactoring
- Verify performance isn't degraded

### Optimization Requests

- Profile before optimizing
- Focus on bottlenecks, not micro-optimizations
- Consider maintainability vs performance tradeoffs
- Document optimization decisions

## Original Implementation Checklist (Completed ✅)

- ✅ Add pytest and a unit test for /health
- ✅ Create GitHub Actions workflow to run pytest on push
- ✅ Add Dockerfile to run Flask on port 9000
- ✅ Improve index.html with minimal responsive styling
- ✅ Add VS Code task to run Flask command
- ✅ Implement /version returning app, Python, Flask versions
- ✅ Add structured logging and request correlation ID
- ✅ Configure Black and isort; format entire project
- ✅ Add 404 JSON error handler with message field
- ✅ Update README quickstart: run, endpoints, devcontainer notes
