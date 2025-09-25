"""
Windows-specific utilities for Python installation.

Handles downloading and installing Python 3.14.0rc3 on Windows systems.
Follows LIGHTWEIGHT and MODERNIZE principles.
"""

import urllib.request
from pathlib import Path

from ..common import run_command

# Python download URLs for Windows
PYTHON_DOWNLOAD_URLS = {
    "3.14.0rc3": {
        "x64": "https://www.python.org/ftp/python/3.14.0/python-3.14.0rc3-amd64.exe",
        "x86": "https://www.python.org/ftp/python/3.14.0/python-3.14.0rc3.exe",
    }
}


def get_windows_architecture() -> str:
    """Get Windows architecture (x64 or x86)."""
    import platform

    machine = platform.machine().lower()
    if machine in ["amd64", "x86_64"]:
        return "x64"
    elif machine in ["x86", "i386", "i686"]:
        return "x86"
    else:
        return "x64"  # Default fallback


def download_python_installer(version: str = "3.14.0rc3") -> tuple[bool, Path]:
    """
    Download Python installer for Windows.

    Args:
        version: Python version to download.

    Returns:
        Tuple of (success, installer_path).
    """
    arch = get_windows_architecture()
    download_url = PYTHON_DOWNLOAD_URLS[version][arch]
    installer_path = Path.cwd() / f"python-{version}-installer.exe"

    try:
        print(f"Downloading Python installer from {download_url}")
        urllib.request.urlretrieve(download_url, installer_path)
        return True, installer_path
    except Exception as e:
        print(f"Failed to download Python installer: {e}")
        return False, installer_path


def install_python_windows(installer_path: Path) -> bool:
    """
    Install Python on Windows using the downloaded installer.

    Args:
        installer_path: Path to the Python installer executable.

    Returns:
        True if installation was successful, False otherwise.
    """
    install_args = [
        str(installer_path),
        "/quiet",
        "InstallAllUsers=1",
        "PrependPath=1",
        "Include_test=0",
        "Include_launcher=1",
        "InstallLauncherAllUsers=1",
    ]

    print("Running Python installer...")
    return_code, _, stderr = run_command(install_args, capture_output=False)

    if return_code == 0:
        print("Python 3.14.0rc3 installed successfully!")
        return True
    else:
        print(f"Python installation failed: {stderr}")
        return False


def cleanup_installer(installer_path: Path) -> None:
    """Clean up the Python installer file."""
    if installer_path.exists():
        try:
            installer_path.unlink()
            print("Installer cleaned up")
        except Exception:
            print("Warning: Could not clean up installer file")


def install_python_complete() -> bool:
    """Complete Python installation process for Windows."""
    success, installer_path = download_python_installer()

    if not success:
        return False

    try:
        return install_python_windows(installer_path)
    finally:
        cleanup_installer(installer_path)
