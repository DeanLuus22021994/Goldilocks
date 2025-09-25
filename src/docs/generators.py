"""
Content generators for documentation.

Following SRP, this module handles only content generation logic
without data collection or file I/O operations.
"""

import subprocess
from pathlib import Path

from .models import GenerationContext


class StructureContentGenerator:
    """Generates project structure content following SRP."""

    def generate_content(self, context: GenerationContext) -> str:
        """Generate structure document content."""
        tree = self._generate_tree(context.project_root)
        metrics = context.metrics

        content = f"""# Project Structure

Generated on: {context.system_info.timestamp.split('T')[0]} \
{context.system_info.timestamp.split('T')[1][:8]}

## Overview

This document provides a comprehensive overview of the Goldilocks project
structure, following modern development practices and clean architecture
principles.

## Project Metrics

- **Total Files**: {metrics.files_count}
- **Lines of Code**: {metrics.lines_of_code:,}
- **Test Files**: {metrics.test_files}
- **Docker Files**: {metrics.docker_files}
- **GitHub Actions**: {metrics.github_workflows}

## Directory Structure

```
{tree}
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
"""
        return content

    def _generate_tree(self, project_root: Path) -> str:
        """Generate project tree structure."""
        try:
            # Use tree command if available, otherwise fallback to Python
            result = subprocess.run(
                [
                    "tree",
                    "-I",
                    "__pycache__|*.pyc|.git|node_modules",
                    str(project_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return result.stdout
        except FileNotFoundError:
            pass

        # Fallback to Python implementation
        return self._python_tree(project_root)

    def _python_tree(self, project_root: Path) -> str:
        """Fallback tree implementation in Python."""
        lines = []
        ignore_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            ".vscode",
        }
        ignore_files = {"*.pyc", ".DS_Store", "*.log"}

        def should_ignore(path: Path) -> bool:
            """Check if path should be ignored."""
            if path.name in ignore_dirs:
                return True
            return any(path.match(pattern) for pattern in ignore_files)

        def walk_tree(path: Path, prefix: str = "") -> None:
            """Recursively walk directory tree."""
            if should_ignore(path):
                return

            children = sorted(
                [p for p in path.iterdir() if not should_ignore(p)],
                key=lambda p: (p.is_file(), p.name),
            )

            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{child.name}")

                if child.is_dir():
                    extension = "    " if is_last else "│   "
                    walk_tree(child, prefix + extension)

        lines.append(f"{project_root.name}/")
        walk_tree(project_root, "")
        return "\n".join(lines)


class TechnicalContentGenerator:
    """Generates technical documentation content following SRP."""

    def generate_content(self, context: GenerationContext) -> str:
        """Generate technical document content."""
        system_info = context.system_info
        metrics = context.metrics

        content = f"""# Technical Documentation

Generated on: {system_info.timestamp}

## System Information

- **Python**: {system_info.python_version}
- **Flask**: {system_info.flask_version}
- **Docker**: {system_info.docker_version}

## Performance Metrics

- **Total Lines of Code**: {metrics.lines_of_code:,}
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
"""
        return content
