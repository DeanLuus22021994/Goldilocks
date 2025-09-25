"""Goldilocks utility functions and helpers.

Contains shared utilities, helper functions, decorators,
and common tools used across the Goldilocks Flask application.

This module provides:
- String manipulation and formatting utilities
- Date/time processing helpers
- File and path manipulation utilities
- Decorators for common functionality
- Performance measurement and debugging tools
- Validation and sanitization utilities
"""

import functools
import re
import time
from collections.abc import Callable
from typing import Any, TypeVar

__all__: list[str] = [
    "timer",
    "safe_get",
    "format_duration",
    "retry",
    "validate_email",
    "sanitize_filename",
    "generate_slug",
]

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

    # Ensure wrapper has all the same attributes as the original function
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    wrapper.__module__ = func.__module__
    wrapper.__qualname__ = getattr(func, "__qualname__", func.__name__)
    wrapper.__annotations__ = getattr(func, "__annotations__", {})

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


def validate_email(email: str) -> bool:
    """Validate email address format."""
    # More strict regex that doesn't allow consecutive dots
    pattern = (
        r"^[a-zA-Z0-9]([a-zA-Z0-9._%+-]*[a-zA-Z0-9])?@"
        r"[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$"
    )
    if ".." in email:  # Explicitly reject consecutive dots
        return False
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing dangerous characters."""
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(" .")
    # Ensure it's not empty
    if not filename:
        filename = "unnamed"
    return filename


def generate_slug(text: str, max_length: int = 50) -> str:
    """Generate URL-friendly slug from text."""
    # Convert to lowercase and replace spaces/special chars with dashes
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    # Remove leading/trailing dashes
    slug = slug.strip("-")
    # Truncate if too long
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug or "untitled"


def truncate_string(
    text: str, max_length: int = 100, suffix: str = "..."
) -> str:
    """Truncate string with ellipsis if longer than max_length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def is_safe_url(url: str) -> bool:
    """Check if URL is safe for redirect (no external domains)."""
    if not url:
        return False
    # Only allow relative URLs or URLs to same domain
    return url.startswith("/") and not url.startswith("//")


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data like email or phone numbers."""
    if len(data) <= visible_chars:
        return "*" * len(data)
    return data[:visible_chars] + "*" * (len(data) - visible_chars)
