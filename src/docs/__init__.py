"""
Goldilocks Documentation Generation Package.

A modern documentation system following SOLID principles and separation
of concerns. Each module handles a specific responsibility without
cross-cutting concerns.

Modules:
- collectors: Data collection from project sources
- generators: Document content generation
- processors: Content processing and formatting
- models: Data structures and type definitions
- cli: Command-line interface
"""

from importlib.metadata import version

try:
    __version__ = version("goldilocks-docs")
except Exception:
    __version__ = "0.1.0"

__all__ = [
    "__version__",
]
