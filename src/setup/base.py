"""
Base setup manager class with common functionality.

Provides a base class that all platform-specific setup managers inherit from.
Follows SRP and DRY principles.
"""

import os
import sys
from abc import ABC, abstractmethod
from typing import Any

from .common import (
    REQUIRED_PACKAGES,
    check_python_version,
    run_command,
    verify_packages,
)


class BaseSetupManager(ABC):
    """Base class for all platform-specific setup managers."""

    def __init__(self):
        """Initialize the base setup manager."""
        self.platform_info = self._get_platform_info()

    @abstractmethod
    def _get_platform_info(self) -> dict[str, Any]:
        """Get platform-specific information."""
        pass

    @abstractmethod
    def _install_python(self) -> bool:
        """Install the required Python version."""
        pass

    @abstractmethod
    def _install_packages(self) -> bool:
        """Install required Python packages."""
        pass

    @abstractmethod
    def _setup_environment_variables(self) -> bool:
        """Setup platform-specific environment variables."""
        pass

    def _check_python_version(self) -> bool:
        """Check if the required Python version is installed."""
        return check_python_version()

    def _install_base_packages(self) -> bool:
        """Install base packages with common logic."""
        print("Installing required Python packages...")

        # Upgrade pip first
        pip_upgrade_cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ]
        return_code, _, stderr = run_command(pip_upgrade_cmd)

        if return_code != 0:
            print(f"Failed to upgrade pip: {stderr}")
            return False

        # Install packages in batches
        packages_to_install = [f"{package}{version}" for package, version in REQUIRED_PACKAGES.items()]

        batch_size = 5
        for i in range(0, len(packages_to_install), batch_size):
            batch = packages_to_install[i : i + batch_size]

            install_cmd = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--no-cache-dir",
            ] + batch

            return_code, _, stderr = run_command(install_cmd)

            if return_code != 0:
                print(f"Package batch installation failed: {stderr}")
                return False

        print("All packages installed successfully!")
        return True

    def _setup_base_environment(self) -> bool:
        """Setup base environment variables common to all platforms."""
        base_env_vars = {
            "FLASK_APP": "app.py",
            "FLASK_ENV": "development",
            "PYTHONUNBUFFERED": "1",
        }

        for key, value in base_env_vars.items():
            os.environ[key] = value
            print(f"Set {key}={value}")

        return True

    def setup_environment(self, config: dict[str, Any]) -> bool:
        """
        Setup the complete development environment.

        Args:
            config: Configuration dictionary for customization.

        Returns:
            True if setup was successful, False otherwise.
        """
        print(f"Setting up {self.platform_info.get('system', 'unknown')} environment...")

        success = True

        # Check and install Python if needed
        if not self._check_python_version():
            print("Python version requirement not met. Installing...")
            if not self._install_python():
                success = False
        else:
            print(f"Python {sys.version_info[:3]} meets requirements")

        # Install packages
        if not config.get("skip_packages", False):
            if not self._install_packages():
                success = False

        # Setup environment variables
        if not self._setup_environment_variables():
            success = False

        return success

    def verify_environment(self) -> dict[str, bool]:
        """
        Verify that all required components are properly installed.

        Returns:
            Dictionary with verification results for each component.
        """
        results = {"python_version": self._check_python_version()}
        results.update(verify_packages())
        return results
