"""
Common utilities and constants for the setup system.

Provides shared functionality across all platform-specific setup modules.
Follows DRY and STANDARDIZATION principles.
"""

import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

__version__ = "1.0.0"

# Required Python version
REQUIRED_PYTHON_VERSION = (3, 14, 0)

# Required packages and their versions
REQUIRED_PACKAGES = {
    "flask": ">=3.1.0",
    "sqlalchemy": ">=2.0.0",
    "pymysql": ">=1.1.0",
    "python-dotenv": ">=1.0.0",
    "wtforms": ">=3.1.0",
    "flask-wtf": ">=1.2.0",
    "flask-login": ">=0.6.0",
    "flask-sqlalchemy": ">=3.1.0",
    "bcrypt": ">=4.1.0",
    "pytest": ">=8.0.0",
    "pytest-cov": ">=4.0.0",
    "mypy": ">=1.8.0",
    "black": ">=24.0.0",
    "isort": ">=5.13.0",
    "flake8": ">=7.0.0",
    "markitdown": ">=0.0.1a2",
}


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


def run_command(command: list[str], capture_output: bool = True, use_sudo: bool = False) -> tuple[int, str, str]:
    """
    Run a command and return the result.

    Args:
        command: Command to run as list of strings.
        capture_output: Whether to capture stdout and stderr.
        use_sudo: Whether to run with sudo privileges (Linux only).

    Returns:
        Tuple of (return_code, stdout, stderr).
    """
    if use_sudo and platform.system() == "Linux":
        import os

        if os.geteuid() != 0:
            command = ["sudo"] + command

    try:
        if capture_output:
            result = subprocess.run(command, capture_output=True, text=True, timeout=600)
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(command, text=True, timeout=600)
            return result.returncode, "", ""
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def check_python_version() -> bool:
    """Check if the required Python version is installed."""
    current_version = sys.version_info[:3]
    return current_version >= REQUIRED_PYTHON_VERSION


def verify_packages() -> dict[str, bool]:
    """Verify that required packages are installed."""
    results: dict[str, bool] = {}
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.replace("-", "_"))
            results[f"package_{package}"] = True
        except ImportError:
            results[f"package_{package}"] = False
    return results
