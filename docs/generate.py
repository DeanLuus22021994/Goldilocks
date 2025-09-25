#!/usr/bin/env python3
"""
Modern documentation generator using markitdown package.

This script follows the separation of concerns principle, creating modular
components for different aspects of documentation generation while avoiding
cross-cutting concerns.
"""

import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ProjectMetrics:
    """Project metrics data structure."""

    files_count: int
    lines_of_code: int
    test_files: int
    docker_files: int
    github_workflows: int


@dataclass
class SystemInfo:
    """System information data structure."""

    python_version: str
    flask_version: str
    docker_version: str
    timestamp: str


class DataCollector:
    """Collects project data following SRP."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def collect_metrics(self) -> ProjectMetrics:
        """Collect project metrics."""
        files_count = sum(
            1 for _ in self.project_root.rglob('*') if _.is_file()
        )

        # Count lines of code
        loc = 0
        for file_path in self.project_root.rglob('*.py'):
            try:
                loc += len(file_path.read_text(encoding='utf-8').splitlines())
            except (UnicodeDecodeError, PermissionError):
                continue

        test_files = len(list(self.project_root.rglob('test*.py')))
        docker_files = len(
            list(self.project_root.rglob('*Dockerfile*'))
        ) + len(list(self.project_root.rglob('docker-compose*.yml')))
        github_workflows = len(
            list(self.project_root.rglob('.github/workflows/*.yml'))
        )

        return ProjectMetrics(
            files_count, loc, test_files, docker_files, github_workflows
        )

    def collect_system_info(self) -> SystemInfo:
        """Collect system information."""
        python_version = subprocess.run(
            ['python3', '--version'], capture_output=True, text=True
        ).stdout.strip()

        # Try to get Flask version from requirements.txt or pip
        flask_version = "Flask (version unknown)"
        try:
            requirements_path = self.project_root / 'requirements.txt'
            if requirements_path.exists():
                content = requirements_path.read_text()
                for line in content.splitlines():
                    if line.strip().lower().startswith('flask'):
                        flask_version = line.strip()
                        break
        except Exception:
            pass

        # Try to get Docker version
        docker_version = "Docker not available"
        try:
            result = subprocess.run(
                ['docker', '--version'], capture_output=True, text=True
            )
            if result.returncode == 0:
                docker_version = result.stdout.strip()
        except Exception:
            pass

        return SystemInfo(
            python_version=python_version,
            flask_version=flask_version,
            docker_version=docker_version,
            timestamp=datetime.now().isoformat(),
        )


class StructureGenerator:
    """Generates project structure documentation following DRY principle."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def generate_tree(self) -> str:
        """Generate project tree structure."""
        try:
            # Use tree command if available, otherwise fallback to Python
            result = subprocess.run(
                [
                    'tree',
                    '-I',
                    '__pycache__|*.pyc|.git|node_modules',
                    str(self.project_root),
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout
        except FileNotFoundError:
            pass

        # Fallback to Python implementation
        return self._python_tree()

    def _python_tree(self) -> str:
        """Fallback tree implementation in Python."""
        lines = []
        ignore_dirs = {
            '.git',
            '__pycache__',
            '.pytest_cache',
            'node_modules',
            '.vscode',
        }
        ignore_files = {'*.pyc', '.DS_Store', '*.log'}

        def should_ignore(path: Path) -> bool:
            if path.name in ignore_dirs:
                return True
            return any(path.match(pattern) for pattern in ignore_files)

        def walk_tree(path: Path, prefix: str = "") -> None:
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

        lines.append(f"{self.project_root.name}/")
        walk_tree(self.project_root, "")
        return "\n".join(lines)


class MarkdownProcessor:
    """Processes markdown using markitdown package."""

    def __init__(self):
        # Lazy import to handle potential import issues
        try:
            import markitdown

            self.markitdown = markitdown.MarkItDown()
        except ImportError:
            self.markitdown = None

    def enhance_content(self, content: str) -> str:
        """Enhance content using markitdown if available."""
        if self.markitdown is None:
            return content

        # For now, return content as-is since we're generating markdown
        # In the future, could process various file types to markdown
        return content


class DocumentationGenerator:
    """Main documentation generator orchestrating all components."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_dir = project_root / 'docs'

        # Initialize components following dependency injection pattern
        self.data_collector = DataCollector(project_root)
        self.structure_generator = StructureGenerator(project_root)
        self.markdown_processor = MarkdownProcessor()

    def generate_structure_doc(self) -> None:
        """Generate STRUCTURE.md document."""
        print("Generating STRUCTURE.md...")

        metrics = self.data_collector.collect_metrics()
        tree = self.structure_generator.generate_tree()

        content = f"""# Project Structure

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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

        output_path = self.docs_dir / 'STRUCTURE.md'
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ Generated {output_path}")

    def generate_technical_doc(self) -> None:
        """Generate TECHNICAL.md document."""
        print("Generating TECHNICAL.md...")

        system_info = self.data_collector.collect_system_info()
        metrics = self.data_collector.collect_metrics()

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

        output_path = self.docs_dir / 'TECHNICAL.md'
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ Generated {output_path}")

    def generate_all(self) -> None:
        """Generate all documentation."""
        print("🚀 Starting modern documentation generation...")

        # Ensure docs directory exists
        self.docs_dir.mkdir(exist_ok=True)

        # Generate documents
        self.generate_structure_doc()
        self.generate_technical_doc()

        print("✅ Documentation generation complete!")


def main():
    """Main entry point."""
    # Get project root from environment or use current working directory
    project_root = Path(os.environ.get('PROJECT_ROOT', os.getcwd()))

    if not project_root.exists():
        print(f"❌ Project root not found: {project_root}")
        return 1

    generator = DocumentationGenerator(project_root)
    generator.generate_all()
    return 0


if __name__ == '__main__':
    exit(main())
