"""
Windows-specific setup and installation utilities for Goldilocks.

Modular Windows setup manager that handles Python installation,
package management, and system configuration.
Follows MODERNIZE and SEPARATION OF CONCERNS principles.
"""

import os
import platform
import sys
from typing import Any

from ..base import BaseSetupManager
from .python_installer import install_python_complete
from .tools import (
    install_docker_windows,
    install_git_windows,
    verify_windows_tools,
)

__version__ = "1.0.0"


class WindowsSetupManager(BaseSetupManager):
    """Manages Windows-specific setup and installation."""

    def _get_platform_info(self) -> dict[str, Any]:
        """Get Windows-specific platform information."""
        # Determine architecture
        machine = platform.machine().lower()
        if machine in ["amd64", "x86_64"]:
            arch = "x64"
        elif machine in ["x86", "i386", "i686"]:
            arch = "x86"
        else:
            arch = "x64"  # Default fallback

        return {
            "system": "windows",
            "architecture": arch,
            "version": platform.version(),
            "release": platform.release(),
            "python_version": sys.version_info,
            "python_executable": sys.executable,
        }

    def _install_python(self) -> bool:
        """Install Python 3.14.0rc3 on Windows."""
        print("Installing Python 3.14.0rc3...")
        return install_python_complete()

    def _install_packages(self) -> bool:
        """Install required Python packages using pip."""
        return self._install_base_packages()

    def _setup_environment_variables(self) -> bool:
        """Setup Windows-specific environment variables."""
        try:
            # Setup base environment
            if not self._setup_base_environment():
                return False

            # Windows-specific environment variables
            windows_env_vars = {
                "PYTHONPATH": str(os.getcwd()),
            }

            for key, value in windows_env_vars.items():
                os.environ[key] = value
                print(f"Set {key}={value}")

            return True
        except Exception as e:
            print(f"Failed to set environment variables: {e}")
            return False

    def setup_environment(self, config: dict[str, Any]) -> bool:
        """Setup complete Windows development environment."""
        success = super().setup_environment(config)

        # Install system tools if not skipped
        if not config.get("skip_git", False):
            install_git_windows()

        if not config.get("skip_docker", False):
            install_docker_windows()

        if success:
            print("Windows environment setup completed successfully!")
        else:
            print("Windows environment setup completed with some issues.")

        return success

    def verify_environment(self) -> dict[str, bool]:
        """Verify Windows environment setup."""
        results = super().verify_environment()
        results.update(verify_windows_tools())
        return results


# Create global instance
setup_manager = WindowsSetupManager()
