"""
Windows system tools installation utilities.

Handles installation of Git and Docker on Windows systems.
Follows HIGH COMPATIBILITY principles.
"""

from ..common import run_command


def check_git_installed() -> bool:
    """Check if Git is installed on Windows."""
    return_code, _, _ = run_command(["git", "--version"])
    return return_code == 0


def check_docker_installed() -> bool:
    """Check if Docker is installed on Windows."""
    return_code, _, _ = run_command(["docker", "--version"])
    return return_code == 0


def install_git_windows() -> bool:
    """
    Install Git for Windows.

    Note: This provides guidance rather than automatic installation
    due to the complexity of silent Git installation on Windows.

    Returns:
        True if Git is already installed, False if manual installation needed.
    """
    if check_git_installed():
        print("Git is already installed")
        return True

    print("Git not found. Please install Git for Windows manually:")
    print("1. Visit https://git-scm.com/download/windows")
    print("2. Download and run the installer")
    print("3. Use the default installation options")
    return False


def install_docker_windows() -> bool:
    """
    Install Docker Desktop for Windows.

    Note: This provides guidance rather than automatic installation
    due to the complexity of Docker Desktop installation.

    Returns:
        True if Docker is already installed, False if manual installation needed.
    """
    if check_docker_installed():
        print("Docker is already installed")
        return True

    print("Docker not found. Please install Docker Desktop manually:")
    print("1. Visit https://www.docker.com/products/docker-desktop/")
    print("2. Download Docker Desktop for Windows")
    print("3. Run the installer and follow the setup wizard")
    print("4. Restart your computer when prompted")
    return False


def verify_windows_tools() -> dict[str, bool]:
    """Verify Windows-specific tools installation."""
    return {
        "git": check_git_installed(),
        "docker": check_docker_installed(),
    }
