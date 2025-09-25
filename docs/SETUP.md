# Goldilocks Setup System

The Goldilocks setup system provides a comprehensive, modular solution for environment setup across Windows, Linux, and container platforms. This system follows the core principles of **MODERNIZE**, **DRY**, **SRP**, and **SEPARATION OF CONCERNS**.

## Architecture Overview

The setup system is organized into platform-specific modules with shared utilities:

```
src/setup/
├── __init__.py          # Main package interface and platform detection
├── base.py              # Abstract base setup manager
├── common.py            # Shared utilities and constants
├── cli.py               # Command-line interface
├── windows/             # Windows-specific setup components
├── linux/               # Linux-specific setup components
└── container/           # Container-optimized setup components
```

## Core Features

### 🔧 **Cross-Platform Support**

- **Windows**: Python installation, package management, system tools
- **Linux**: Source compilation, multi-distro package management, development tools
- **Container**: Optimization, health checks, minimal footprint setup

### 🏗️ **Modular Architecture**

- **Base Classes**: Abstract setup managers with common functionality
- **Platform Modules**: Specialized implementations for each environment
- **Shared Utilities**: Common functions and constants (DRY principle)

### ⚡ **Smart Detection**

- Automatic platform detection (Windows/Linux/Container/WSL)
- Package manager detection (apt/yum/dnf/pacman/zypper)
- Environment capability assessment

## Quick Start

### Python API

```python
from src.setup import setup_environment, verify_environment, get_platform_info

# Get platform information
platform_info = get_platform_info()
print(f"Platform: {platform_info['system']}")

# Setup environment with default configuration
success = setup_environment()

# Verify installation
results = verify_environment()
print(f"Verification: {sum(results.values())}/{len(results)} passed")
```

### Command Line Interface

```bash
# Setup with interactive prompts
python src/setup/cli.py setup

# Quick setup with defaults
python src/setup/cli.py setup --quick

# Verify environment
python src/setup/cli.py verify

# Get platform information
python src/setup/cli.py info
```

## Platform-Specific Components

### Windows Module (`src/setup/windows/`)

- **`__init__.py`**: WindowsSetupManager - Main setup orchestration
- **`python_installer.py`**: Python 3.14.0rc3 download and installation utilities
- **`tools.py`**: Git, Docker, and development tools management

**Key Features:**

- Automated Python installer download (x64/x86 support)
- Silent installation with proper PATH configuration
- System tools verification and guidance

### Linux Module (`src/setup/linux/`)

- **`__init__.py`**: LinuxSetupManager - Main setup orchestration
- **`python_builder.py`**: Python source compilation and build management
- **`package_manager.py`**: Multi-distribution package management
- **`tools.py`**: Development tools installation and verification

**Key Features:**

- Multi-distro support (Ubuntu, CentOS, Fedora, Arch, openSUSE)
- Python source compilation with optimizations
- Package manager abstraction layer

### Container Module (`src/setup/container/`)

- **`__init__.py`**: ContainerSetupManager - Lightweight setup orchestration
- **`optimizer.py`**: Container size and performance optimization
- **`health_checks.py`**: Readiness and liveness verification

**Key Features:**

- Cache cleanup and size optimization
- Health check endpoints
- Minimal environment configuration

## Configuration Options

### Setup Configuration

```python
config = {
    "skip_python": False,      # Skip Python installation
    "skip_packages": False,    # Skip package installation
    "skip_git": False,         # Skip Git installation (Windows/Linux)
    "skip_docker": False,      # Skip Docker installation (Windows/Linux)
    "skip_tools": False,       # Skip development tools (Linux)
    "skip_optimization": False # Skip container optimization (Container)
}

setup_environment(config)
```

### Environment Variables

The setup system respects these environment variables:

- `PYTHON_VERSION`: Override target Python version
- `SKIP_SYSTEM_PACKAGES`: Skip system package installation
- `CONTAINER_OPTIMIZED`: Enable container-specific optimizations

## Development Principles

### **MODERNIZE**

- Latest Python features (3.12+ type hints)
- Current best practices and tooling
- Modern package management approaches

### **DRY (Don't Repeat Yourself)**

- Shared utilities in `common.py`
- Base classes for common functionality
- Abstract platform-specific implementations

### **SRP (Single Responsibility Principle)**

- Each module handles one specific aspect
- Clear separation between installation, verification, and optimization
- Platform-specific concerns isolated

### **SEPARATION OF CONCERNS**

- Platform detection separate from setup logic
- Installation separate from verification
- No cross-cutting dependencies

## Testing and Verification

### Verification Checks

Each platform manager provides comprehensive verification:

```python
results = verify_environment()

# Common checks across all platforms
assert results["python_version"]     # Python version compatibility
assert results["pip_available"]     # Package installer availability
assert results["base_packages"]     # Required packages installed

# Platform-specific checks
# Windows: git, docker verification
# Linux: git, docker, nodejs verification
# Container: health checks, readiness verification
```

### Health Checks (Container)

The container module provides detailed health checking:

- **Python Environment**: Version compatibility, pip availability
- **Required Packages**: Flask, SQLAlchemy, and dependencies
- **File Permissions**: Write access and application files
- **Network Connectivity**: Basic network access
- **Application Startup**: Module loading verification

## Advanced Usage

### Custom Setup Managers

Extend the base setup manager for custom environments:

```python
from src.setup.base import BaseSetupManager

class CustomSetupManager(BaseSetupManager):
    def _get_platform_info(self):
        return {"system": "custom", ...}

    def _install_python(self):
        # Custom Python installation logic
        return True

    def _install_packages(self):
        return self._install_base_packages()
```

### Integration with CI/CD

The setup system integrates well with automated workflows:

```yaml
# GitHub Actions example
- name: Setup Environment
  run: |
    python src/setup/cli.py setup --quick
    python src/setup/cli.py verify
```

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure proper sudo/admin privileges
2. **Network Issues**: Check firewall and proxy settings
3. **Package Conflicts**: Clean package caches and retry
4. **Platform Detection**: Verify environment variables and file system

### Debugging

Enable verbose output for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from src.setup import setup_environment
setup_environment({"verbose": True})
```

## Contributing

When extending the setup system:

1. Follow the established modular pattern
2. Add platform-specific code to appropriate modules
3. Update verification functions for new capabilities
4. Maintain <100 lines per module for readability
5. Add comprehensive docstrings and type hints

## License

This setup system is part of the Goldilocks project and follows the same licensing terms.
