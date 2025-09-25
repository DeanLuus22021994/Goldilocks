"""
Container-specific setup and installation utilities for Goldilocks.

Modular container setup manager that handles Python environment setup,
package installation, and container-optimized configuration.
Follows MODERNIZE, LIGHTWEIGHT, and LOW FOOTPRINT principles.
"""

import os
import sys
from typing import Any

from ..base import BaseSetupManager
from .health_checks import is_container_ready, run_health_checks
from .optimizer import optimize_container

__version__ = "1.0.0"


class ContainerSetupManager(BaseSetupManager):
    """Manages container-specific setup and installation."""

    def _get_platform_info(self) -> dict[str, Any]:
        """Get container-specific platform information."""
        import platform

        return {
            "system": "container",
            "architecture": platform.machine(),
            "python_version": sys.version_info,
            "python_executable": sys.executable,
            "container_id": os.environ.get("HOSTNAME", "unknown"),
            "image_name": os.environ.get("IMAGE_NAME", "unknown"),
        }

    def _install_python(self) -> bool:
        """Python should already be installed in container."""
        print("Python is pre-installed in container")
        return True

    def _install_packages(self) -> bool:
        """Install required Python packages using pip."""
        return self._install_base_packages()

    def _setup_environment_variables(self) -> bool:
        """Setup container-specific environment variables."""
        try:
            # Setup base environment
            if not self._setup_base_environment():
                return False

            # Container-specific environment variables
            container_env_vars = {
                "PYTHONUNBUFFERED": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "random",
                "PIP_NO_CACHE_DIR": "1",
                "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            }

            for key, value in container_env_vars.items():
                os.environ[key] = value
                print(f"Set {key}={value}")

            return True
        except Exception as e:
            print(f"Failed to set environment variables: {e}")
            return False

    def setup_environment(self, config: dict[str, Any]) -> bool:
        """Setup complete container development environment."""
        success = super().setup_environment(config)

        # Run container optimizations if not skipped
        if not config.get("skip_optimization", False):
            optimize_container()

        if success:
            print("Container environment setup completed successfully!")
        else:
            print("Container environment setup completed with some issues.")

        return success

    def verify_environment(self) -> dict[str, bool]:
        """Verify container environment setup."""
        results = super().verify_environment()

        # Add container-specific checks
        health_results = run_health_checks()
        results.update(health_results)

        # Add overall readiness check
        results["container_ready"] = is_container_ready()

        return results


# Create global instance
setup_manager = ContainerSetupManager()
