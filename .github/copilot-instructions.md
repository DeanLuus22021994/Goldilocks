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

## AI-Powered Development Workflow

### Copilot Agent Mode Usage

- Use Agent Mode for complex, multi-file refactoring tasks
- Enable autonomous edits across the entire codebase when requested
- Allow agent to determine relevant context and files automatically
- Use high-level requirements like "refactor auth to use OAuth" or "add Redis caching"
- Leverage automatic issue resolution and iteration capabilities
- Enable todo list tracking for complex feature implementation

### Context-Aware Code Generation

- Always include relevant file context when making changes
- Reference related files using Markdown links in prompts
- Use workspace-specific patterns and established conventions
- Maintain consistency with existing code architecture
- Apply project-specific naming conventions and patterns

### Iterative Development Approach

- Start with high-level feature descriptions
- Allow Copilot to break down complex tasks into manageable steps
- Review and approve each iteration before proceeding
- Use chat checkpoints to revert to previous stable states
- Leverage auto-fix capabilities for syntax and test errors

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
- **Security-first** - Validate all inputs, use secure defaults, no hardcoded secrets

### Development Workflow

- **Pre-commit hooks** - Automated formatting and linting before commits
- **CI/CD validation** - All tests, linting, type checking must pass
- **Branch protection** - No direct commits to main, require PR reviews
- **Semantic commits** - Clear, descriptive commit messages
- **Automated testing** - Run tests before and after AI-generated changes

### Performance & Efficiency

- **Minimal dependencies** - Only include necessary packages
- **Optimized Docker** - Multi-stage builds, minimal base images, layer caching
- **Resource efficiency** - Monitor memory usage, startup time, response times
- **Caching strategies** - Leverage pip cache, Docker layer cache, application caching

## Python-Specific Guidelines

### Modern Python Practices

- Use Python 3.12+ features and type system enhancements
- Prefer `match` statements over complex if/elif chains
- Use dataclasses and Pydantic for data models
- Implement proper error handling with custom exceptions
- Use context managers for resource management

### Flask Application Structure

- Follow blueprint organization for large applications
- Implement proper request/response handling
- Use dependency injection for service classes
- Maintain clean separation between routes and business logic
- Implement comprehensive logging and monitoring

### Testing Standards

- Write pytest-compatible tests with clear naming
- Use fixtures for test data and common setup
- Mock external dependencies and services
- Test both success and failure scenarios
- Maintain test isolation and independence

## Container & DevOps Guidelines

### Docker Best Practices

- Use multi-stage builds for production optimization
- Implement proper layer caching strategies
- Run containers as non-root users
- Use specific base image versions, not `latest`
- Optimize image size with minimal dependencies

### Development Environment

- Maintain consistent dev container configuration
- Use VS Code tasks for common development operations
- Configure proper debugging and profiling tools
- Implement hot-reload for development efficiency
- Maintain environment parity across dev/test/prod

## Security & Compliance

### Security Best Practices

- **Input validation** - Sanitize and validate all user inputs
- **Authentication** - Implement secure authentication patterns
- **Authorization** - Use role-based access control
- **Data protection** - Encrypt sensitive data at rest and in transit
- **Dependency scanning** - Regular security updates via Dependabot

### Compliance Requirements

- Follow OWASP security guidelines
- Implement proper logging for audit trails
- Use secure communication protocols (HTTPS, TLS)
- Regular security assessments and penetration testing
- Maintain security documentation and incident response plans

## Documentation Standards

### Code Documentation

- **Docstrings** - Comprehensive function and class documentation
- **Type hints** - Complete type annotations for all public APIs
- **Inline comments** - Explain complex business logic and algorithms
- **API documentation** - Auto-generated from code annotations
- **Architecture decisions** - Document significant technical choices

### User Documentation

- **README first** - Clear setup and usage instructions
- **Getting started** - Step-by-step onboarding guide
- **API reference** - Complete endpoint documentation
- **Troubleshooting** - Common issues and solutions
- **Contributing guide** - Development workflow and standards

## AI Development Guidelines

### Prompt Engineering

- Be specific about requirements and constraints
- Include relevant context and examples
- Request explanations for complex implementations
- Ask for multiple approaches when appropriate
- Validate generated code before integration

### Code Review with AI

- Use AI for initial code review and suggestions
- Focus on architecture, security, and performance
- Verify adherence to project conventions
- Check for proper error handling and edge cases
- Ensure comprehensive test coverage

### Continuous Learning

- Stay updated with latest Python and Flask features
- Learn from AI-generated code patterns
- Share knowledge through documentation updates
- Experiment with new development approaches
- Contribute improvements back to the project

## Quality Assurance

### Automated Quality Checks

- **Linting** - flake8, mypy, black, isort compliance
- **Testing** - Comprehensive test suite with coverage reporting
- **Security** - Automated vulnerability scanning
- **Performance** - Benchmarking and profiling tools
- **Dependencies** - Regular updates and compatibility checks

### Manual Quality Reviews

- **Code review** - Peer review of all changes
- **Architecture review** - Periodic architecture assessments
- **Security review** - Regular security audits
- **Performance review** - Optimization opportunities
- **Documentation review** - Keep documentation current and accurate

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
- ✅ Update README quickstart: run, endpoints, devcontainer notess
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
