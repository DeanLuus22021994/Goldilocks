# Technical Documentation

Generated on: 2025-09-25T13:15:53.275632

## System Information

- **Python**: Python 3.12.3
- **Flask**: Flask==3.1.2
- **Docker**: Docker version 28.1.1, build 4eba377

## Performance Metrics

- **Total Lines of Code**: 6,567
- **Test Coverage Target**: 100%
- **Build Time**: Optimized for fast startup
- **Memory Footprint**: Minimal resource usage

## Technology Stack

### Core Framework
- **Flask**: Lightweight web framework
- **Python 3.x**: Modern Python with type hints

### Development Tools
- **pytest**: Testing framework
- **mypy**: Static type checking
- **black**: Code formatting
- **isort**: Import sorting
- **pre-commit**: Git hooks for quality

### Container Technology
- **Docker**: Containerized development and deployment
- **Multi-stage builds**: Optimized image size
- **Alpine Linux**: Minimal base images

### Documentation
- **markitdown**: Modern markdown processing
- **VS Code MCP**: Model Context Protocol integration
- **Automated generation**: Dynamic content creation

## Quality Assurance

### Code Standards
- Type hints for all functions
- 100% test coverage requirement
- Linting compliance (flake8, mypy, black)
- Pre-commit validation

### Security
- No secrets in code
- Dependency scanning via Dependabot
- Container security best practices
- Input validation and sanitization

### Performance
- Minimal dependencies
- Optimized Docker layers
- Efficient resource usage
- Fast application startup

## Deployment

### Local Development
```bash
# Start development environment
make dev

# Run tests
make test

# Format code
make format
```

### Docker Deployment
```bash
# Build optimized image
docker build -t goldilocks .

# Run production container
docker run -p 9000:9000 goldilocks
```

### CI/CD Pipeline
- Automated testing on every commit
- Docker image builds
- Security scanning
- Performance monitoring

## Monitoring

### Health Checks
- `/health` endpoint for service monitoring
- `/version` endpoint for version information
- Structured JSON logging

### Metrics
- Request correlation IDs
- Performance timing headers
- Resource usage monitoring

## Architecture Decisions

### Separation of Concerns
- Clean separation between modules
- No cross-cutting functionality
- Well-defined interfaces

### Documentation Strategy
- Automated generation using markitdown
- VS Code integration via MCP servers
- Dynamic content based on project state

This technical documentation is automatically maintained to reflect
the current state of the project and follows modern development practices.
