"""
Linux-specific Python installation and build utilities.

Handles Python 3.14.0rc3 installation from source on Linux systems.
Follows MODERNIZE and HIGH COMPATIBILITY principles.
"""

import subprocess
import sys
from pathlib import Path

from ..common import REQUIRED_PYTHON_VERSION, run_command

__version__ = "1.0.0"

# Python source download information
PYTHON_SOURCE_URL = "https://www.python.org/ftp/python/3.14.0/Python-3.14.0rc3.tgz"
BUILD_DEPENDENCIES = [
    "build-essential",
    "zlib1g-dev",
    "libncurses5-dev",
    "libgdbm-dev",
    "libnss3-dev",
    "libssl-dev",
    "libreadline-dev",
    "libffi-dev",
    "libsqlite3-dev",
    "wget",
    "libbz2-dev",
    "libgdbm-compat-dev",
    "liblzma-dev",
    "uuid-dev",
]


def install_build_dependencies() -> bool:
    """Install build dependencies for Python compilation."""
    print("Installing Python build dependencies...")

    # Update package list first
    if not run_command(["sudo", "apt", "update"]):
        print("Failed to update package list")
        return False

    # Install build dependencies
    cmd = ["sudo", "apt", "install", "-y"] + BUILD_DEPENDENCIES
    if not run_command(cmd):
        print("Failed to install build dependencies")
        return False

    print("Build dependencies installed successfully")
    return True


def download_python_source() -> tuple[bool, Path]:
    """Download Python source code."""
    print("Downloading Python 3.14.0rc3 source...")

    source_dir = Path.cwd() / "python-source"
    source_dir.mkdir(exist_ok=True)

    tarball_path = source_dir / "Python-3.14.0rc3.tgz"

    # Download source
    cmd = ["wget", "-O", str(tarball_path), PYTHON_SOURCE_URL]
    if not run_command(cmd):
        print("Failed to download Python source")
        return False, tarball_path

    print("Python source downloaded successfully")
    return True, tarball_path


def extract_and_build_python(tarball_path: Path) -> bool:
    """Extract and build Python from source."""
    print("Extracting and building Python...")

    source_dir = tarball_path.parent

    # Extract tarball
    cmd = ["tar", "-xzf", str(tarball_path), "-C", str(source_dir)]
    if not run_command(cmd):
        print("Failed to extract Python source")
        return False

    # Navigate to source directory
    python_src_dir = source_dir / "Python-3.14.0rc3"
    if not python_src_dir.exists():
        print("Python source directory not found")
        return False

    # Configure build
    print("Configuring Python build...")
    try:
        result = subprocess.run(
            [
                "./configure",
                "--enable-optimizations",
                "--with-ensurepip=install",
            ],
            cwd=python_src_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            print(f"Failed to configure Python build: {result.stderr}")
            return False
    except Exception as e:
        print(f"Failed to configure Python build: {e}")
        return False

    # Build Python
    print("Building Python (this may take several minutes)...")
    try:
        result = subprocess.run(
            ["make", "-j4"],
            cwd=python_src_dir,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 minutes
        )
        if result.returncode != 0:
            print(f"Failed to build Python: {result.stderr}")
            return False
    except Exception as e:
        print(f"Failed to build Python: {e}")
        return False

    # Install Python
    print("Installing Python...")
    try:
        result = subprocess.run(
            ["sudo", "make", "altinstall"],
            cwd=python_src_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            print(f"Failed to install Python: {result.stderr}")
            return False
    except Exception as e:
        print(f"Failed to install Python: {e}")
        return False

    print("Python 3.14.0rc3 built and installed successfully")
    return True


def verify_python_installation() -> bool:
    """Verify that Python 3.14 was installed correctly."""
    try:
        # Check if python3.14 is available
        result = subprocess.run(
            ["python3.14", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print(f"Python verification successful: {result.stdout.strip()}")
            return True
        else:
            print("Python 3.14 not found in PATH")
            return False

    except Exception as e:
        print(f"Failed to verify Python installation: {e}")
        return False


def install_python_complete() -> bool:
    """Complete Python installation process for Linux."""
    print("Starting Python 3.14.0rc3 installation on Linux...")

    # Check if Python is already installed
    current_version = sys.version_info[:3]
    if current_version >= REQUIRED_PYTHON_VERSION:
        print(f"Python {current_version} is already installed")
        return True

    # Install build dependencies
    if not install_build_dependencies():
        return False

    # Download source
    success, tarball_path = download_python_source()
    if not success:
        return False

    # Extract and build
    if not extract_and_build_python(tarball_path):
        return False

    # Verify installation
    if not verify_python_installation():
        return False

    # Clean up source files
    try:
        import shutil

        shutil.rmtree(tarball_path.parent)
        print("Cleaned up source files")
    except Exception:
        print("Warning: Failed to clean up source files")

    print("Python 3.14.0rc3 installation completed successfully!")
    return True
