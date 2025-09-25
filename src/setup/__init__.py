"""
Cross-platform setup and installation system for Goldilocks.

This package provides environment-specific setup utilities that ensure
consistent installation across Windows, Linux, and container environments.
Follows MODERNIZE, HIGH COMPATIBILITY, and STANDARDIZATION principles.
"""

import platform
import sys
from pathlib import Path
from typing import Any

__version__ = "1.0.0"


def get_platform_info() -> dict[str, Any]:
    """Get comprehensive platform information."""
    return {
        "system": platform.system().lower(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "python_version": sys.version_info,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "is_container": Path("/.dockerenv").exists(),
        "is_wsl": ("microsoft" in platform.release().lower() if platform.system() == "Linux" else False),
    }


def get_setup_module():
    """
    Get the appropriate setup module based on the current environment.

    Returns:
        The appropriate setup module for the current platform.
    """
    platform_info = get_platform_info()

    # Determine environment type
    if platform_info["is_container"]:
        from .container import setup_manager

        return setup_manager
    elif platform_info["system"] == "windows":
        from .windows import setup_manager

        return setup_manager
    elif platform_info["system"] == "linux":
        from .linux import setup_manager

        return setup_manager
    else:
        # Fallback to Linux for Unix-like systems
        from .linux import setup_manager

        return setup_manager


def setup_environment(config: dict[str, Any] | None = None) -> bool:
    """
    Setup the environment based on the current platform.

    Args:
        config: Optional configuration dictionary for setup customization.

    Returns:
        True if setup was successful, False otherwise.
    """
    try:
        setup_module = get_setup_module()
        return setup_module.setup_environment(config or {})
    except Exception as e:
        print(f"Setup failed: {e}")
        return False


def verify_environment() -> dict[str, bool]:
    """
    Verify that all required components are properly installed.

    Returns:
        Dictionary with verification results for each component.
    """
    try:
        setup_module = get_setup_module()
        return setup_module.verify_environment()
    except Exception as e:
        print(f"Verification failed: {e}")
        return {"error": False}
