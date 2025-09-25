"""
Container optimization utilities for Goldilocks.

Handles container-specific optimizations, cache management,
and resource efficiency improvements.
Follows LIGHTWEIGHT and LOW FOOTPRINT principles.
"""

import os
import shutil
import subprocess
from pathlib import Path

__version__ = "1.0.0"


def clean_package_cache() -> bool:
    """Clean package manager caches to reduce container size."""
    print("Cleaning package manager caches...")

    try:
        # Clean apt cache if it exists
        if shutil.which("apt"):
            subprocess.run(["apt", "clean"], check=False)
            subprocess.run(["apt", "autoremove", "-y"], check=False)

        # Clean pip cache
        if shutil.which("pip"):
            subprocess.run(["pip", "cache", "purge"], check=False)

        # Remove pip cache directory if it exists
        pip_cache_dir = Path.home() / ".cache" / "pip"
        if pip_cache_dir.exists():
            shutil.rmtree(pip_cache_dir)

        print("Package caches cleaned successfully")
        return True

    except Exception as e:
        print(f"Warning: Failed to clean package caches: {e}")
        return False


def remove_unnecessary_files() -> bool:
    """Remove unnecessary files to reduce container image size."""
    print("Removing unnecessary files...")

    files_to_remove = [
        "/var/lib/apt/lists/*",
        "/tmp/*",
        "/var/tmp/*",
        "**/*.pyc",
        "**/__pycache__",
        "**/*.pyo",
        "**/*.egg-info",
    ]

    try:
        for pattern in files_to_remove:
            if "*" in pattern:
                # Use shell for glob patterns
                subprocess.run(f"rm -rf {pattern}", shell=True, check=False)
            else:
                path = Path(pattern)
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()

        print("Unnecessary files removed successfully")
        return True

    except Exception as e:
        print(f"Warning: Failed to remove unnecessary files: {e}")
        return False


def optimize_python_bytecode() -> bool:
    """Optimize Python bytecode compilation."""
    print("Optimizing Python bytecode...")

    try:
        # Compile Python files to bytecode
        result = subprocess.run(
            ["python", "-m", "compileall", "-b", "."],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("Python bytecode compiled successfully")
            return True
        else:
            print(f"Failed to compile bytecode: {result.stderr}")
            return False

    except Exception as e:
        print(f"Warning: Failed to optimize bytecode: {e}")
        return False


def setup_minimal_environment() -> bool:
    """Setup minimal environment variables for containers."""
    print("Setting up minimal container environment...")

    try:
        # Container-optimized environment variables
        container_env_vars = {
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "random",
            "PIP_NO_CACHE_DIR": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        }

        for key, value in container_env_vars.items():
            os.environ[key] = value

        print("Container environment variables set")
        return True

    except Exception as e:
        print(f"Failed to set container environment: {e}")
        return False


def get_container_stats() -> dict[str, str]:
    """Get container resource statistics."""
    stats: dict[str, str] = {}

    try:
        # Get disk usage
        result = subprocess.run(["du", "-sh", "."], capture_output=True, text=True)

        if result.returncode == 0:
            stats["disk_usage"] = result.stdout.strip().split()[0]

        # Get memory info if available
        if Path("/proc/meminfo").exists():
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemAvailable:"):
                        stats["memory_available"] = line.split()[1] + " kB"
                        break

        return stats

    except Exception as e:
        print(f"Warning: Could not get container stats: {e}")
        return {}


def optimize_container() -> bool:
    """Run all container optimizations."""
    print("Running container optimizations...")

    results: list[bool] = []
    results.append(clean_package_cache())
    results.append(remove_unnecessary_files())
    results.append(optimize_python_bytecode())
    results.append(setup_minimal_environment())

    success = all(results)

    if success:
        print("Container optimizations completed successfully!")
        stats = get_container_stats()
        if stats:
            print("Container stats:", stats)
    else:
        print("Some optimizations may have failed.")

    return success
