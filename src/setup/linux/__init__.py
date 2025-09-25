"""
Linux-specific setup and installation utilities for Goldilocks.

Modular Linux setup manager that handles Python installation,
package management, and system configuration.
Follows MODERNIZE and SEPARATION OF CONCERNS principles.
"""

import os
import sys
from typing import Any

from ..base import BaseSetupManager
from .package_manager import install_development_environment
from .python_builder import install_python_complete
from .tools import install_all_tools, verify_linux_tools

__version__ = "1.0.0"


class LinuxSetupManager(BaseSetupManager):
    """Manages Linux-specific setup and installation."""

    def _get_platform_info(self) -> dict[str, Any]:
        """Get Linux-specific platform information."""
        import platform

        try:
            # Try to get distribution info
            os_release: dict[str, str] = {}
            with open("/etc/os-release") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        os_release[key] = value.strip('"')

            distro = os_release.get("ID", "unknown")
            version = os_release.get("VERSION_ID", "unknown")
        except Exception:
            distro = "unknown"
            version = "unknown"

        return {
            "system": "linux",
            "distribution": distro,
            "version": version,
            "architecture": platform.machine(),
            "kernel": platform.release(),
            "python_version": sys.version_info,
            "python_executable": sys.executable,
        }

    def _install_python(self) -> bool:
        """Install Python 3.14.0rc3 on Linux."""
        print("Installing Python 3.14.0rc3...")
        return install_python_complete()

    def _install_packages(self) -> bool:
        """Install required Python packages using pip."""
        return self._install_base_packages()

    def _setup_environment_variables(self) -> bool:
        """Setup Linux-specific environment variables."""
        try:
            # Setup base environment
            if not self._setup_base_environment():
                return False

            # Linux-specific environment variables
            linux_env_vars = {
                "PYTHONPATH": str(os.getcwd()),
                "PATH": f"{os.environ.get('PATH', '')}:/usr/local/bin",
            }

            for key, value in linux_env_vars.items():
                os.environ[key] = value
                print(f"Set {key}={value}")

            return True
        except Exception as e:
            print(f"Failed to set environment variables: {e}")
            return False

    def setup_environment(self, config: dict[str, Any]) -> bool:
        """Setup complete Linux development environment."""
        # Install development environment first
        if not config.get("skip_system_packages", False):
            print("Installing development environment...")
            install_development_environment()

        # Run base setup
        success = super().setup_environment(config)

        # Install development tools if not skipped
        if not config.get("skip_tools", False):
            install_all_tools()

        if success:
            print("Linux environment setup completed successfully!")
        else:
            print("Linux environment setup completed with some issues.")

        return success

    def verify_environment(self) -> dict[str, bool]:
        """Verify Linux environment setup."""
        results = super().verify_environment()
        results.update(verify_linux_tools())
        return results


# Create global instance
setup_manager = LinuxSetupManager()
