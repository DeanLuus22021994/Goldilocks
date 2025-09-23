"""Goldilocks core functionality.

Contains the core business logic, configuration management,
and shared utilities for the Goldilocks Flask application.

This module provides:
- Configuration management and environment setup
- Core application utilities and helpers
- Shared constants and application state management
- Base classes for business logic components
"""

from typing import Any

__all__: list[str] = ["DEFAULT_CONFIG", "PACKAGE_INFO", "get_config"]

# Core configuration constants
DEFAULT_CONFIG = {
    "FLASK_APP": "goldilocks.app",
    "FLASK_ENV": "production",
    "LOG_LEVEL": "INFO",
    "REQUEST_TIMEOUT": 30,
    "MAX_CONTENT_LENGTH": 16 * 1024 * 1024,  # 16MB
}

# Application metadata for introspection
PACKAGE_INFO = {
    "name": "goldilocks",
    "description": "High-performance Flask application with optimization",
    "author": "Goldilocks Development Team",
    "license": "MIT",
}


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value with fallback to default."""
    return DEFAULT_CONFIG.get(key, default)
