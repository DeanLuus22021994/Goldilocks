"""Goldilocks Flask application package.

A high-performance Flask application with optimized architecture,
comprehensive testing, and modern development practices.

Exports package metadata used by tooling and for introspection.
"""

from goldilocks.app import app
from goldilocks.core import DEFAULT_CONFIG, PACKAGE_INFO, get_config

__version__ = "1.0.0"
__author__ = "Goldilocks Development Team"
__license__ = "MIT"
__description__ = "High-performance Flask application with optimization"

__all__ = [
    "app",
    "DEFAULT_CONFIG",
    "PACKAGE_INFO",
    "get_config",
    "__version__",
    "__author__",
    "__license__",
    "__description__",
]
