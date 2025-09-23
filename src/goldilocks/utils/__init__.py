"""Goldilocks utility functions and helpers.

Contains shared utilities, helper functions, decorators,
and common tools used across the Goldilocks Flask application.

This module provides:
- String manipulation and formatting utilities
- Date/time processing helpers
- File and path manipulation utilities
- Decorators for common functionality
- Performance measurement and debugging tools
"""

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

__all__: list[str] = ["timer", "safe_get", "format_duration", "retry"]

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """Decorator to measure function execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds")
        return result

    return wrapper  # type: ignore


def safe_get(dictionary: dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with default fallback."""
    return dictionary.get(key, default)


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 1:
        return f"{seconds * 1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f}m"
    else:
        return f"{seconds / 3600:.1f}h"


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    """Decorator to retry function execution on failure."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    continue
            raise last_exception or RuntimeError("Retry failed")

        return wrapper  # type: ignore

    return decorator
