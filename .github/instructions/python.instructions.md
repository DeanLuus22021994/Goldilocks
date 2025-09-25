---
applyTo: "**/*.py"
description: "Python-specific coding standards and best practices for Goldilocks"
---

# Python Development Instructions

## Type Annotations

- Always use type hints for function parameters and return values
- Use `from typing import` for complex types like `Dict`, `List`, `Optional`, `Union`
- Use `from __future__ import annotations` for forward references when needed
- Prefer `dict[str, Any]` over `Dict[str, Any]` for Python 3.9+
- Use `| None` instead of `Optional[T]` for Python 3.10+

## Code Style

- Follow PEP 8 style guidelines strictly
- Use Black for automatic code formatting
- Line length maximum of 88 characters (Black default)
- Use double quotes for strings unless single quotes avoid escaping
- Prefer f-strings for string formatting over `.format()` or `%` formatting

## Function and Class Design

- Keep functions focused and under 20 lines when possible
- Use descriptive function and variable names
- Write comprehensive docstrings using Google style
- Use dataclasses or Pydantic models for data structures
- Implement `__str__` and `__repr__` methods for custom classes

## Error Handling

- Use specific exception types, avoid bare `except:` clauses
- Create custom exception classes when appropriate
- Use context managers for resource management
- Log exceptions with appropriate context information
- Fail fast with clear error messages

## Imports Organization

- Group imports in this order: standard library, third-party, local imports
- Use absolute imports for clarity
- Avoid wildcard imports (`from module import *`)
- Sort imports alphabetically within each group
- Use isort for automatic import organization

## Testing Standards

- Write tests for all public functions and methods
- Use pytest fixtures for test setup and teardown
- Mock external dependencies and I/O operations
- Test both success and failure scenarios
- Aim for 100% test coverage with meaningful assertions

## Performance Considerations

- Use list comprehensions and generator expressions appropriately
- Prefer `pathlib` over `os.path` for file operations
- Use `enumerate()` instead of manual counter variables
- Consider memory usage for large data sets
- Profile code before optimizing

## Flask-Specific Patterns

- Use blueprints for organizing routes
- Implement proper error handlers
- Use Flask's application factory pattern
- Validate request data with schemas
- Implement proper logging and monitoring
- Use Flask-Login for authentication management
- Implement CSRF protection for forms
