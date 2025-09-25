"""
Linux system tools installation and verification utilities.

Handles installation of development tools like Git, Docker, and IDE setup.
Follows MODERNIZE and SEPARATION OF CONCERNS principles.
"""

import subprocess

from .package_manager import install_system_packages

__version__ = "1.0.0"


def check_git_installed() -> bool:
    """Check if Git is installed on the system."""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False


def install_git_linux() -> bool:
    """Install Git on Linux systems."""
    if check_git_installed():
        print("Git is already installed")
        return True

    print("Installing Git...")
    return install_system_packages(["git"])


def check_docker_installed() -> bool:
    """Check if Docker is installed on the system."""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False


def install_docker_linux() -> bool:
    """Install Docker on Linux systems."""
    if check_docker_installed():
        print("Docker is already installed")
        return True

    print("Installing Docker...")
    print("Note: This installs docker.io package. For Docker CE, use official Docker repository")

    # Install docker.io package (basic Docker installation)
    success = install_system_packages(["docker.io"])

    if success:
        print("Docker installed. Adding current user to docker group...")
        try:
            # Add user to docker group
            result = subprocess.run(
                ["sudo", "usermod", "-aG", "docker", "$USER"],
                capture_output=True,
                timeout=30,
            )

            if result.returncode == 0:
                print("User added to docker group. Please log out and back in to apply changes.")
            else:
                print("Warning: Failed to add user to docker group")
        except Exception as e:
            print(f"Warning: Failed to configure docker group: {e}")

    return success


def check_nodejs_installed() -> bool:
    """Check if Node.js is installed on the system."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False


def install_nodejs_linux() -> bool:
    """Install Node.js on Linux systems."""
    if check_nodejs_installed():
        print("Node.js is already installed")
        return True

    print("Installing Node.js...")
    return install_system_packages(["nodejs", "npm"])


def verify_linux_tools() -> dict[str, bool]:
    """Verify installation status of Linux development tools."""
    return {
        "git": check_git_installed(),
        "docker": check_docker_installed(),
        "nodejs": check_nodejs_installed(),
    }


def install_all_tools() -> bool:
    """Install all common development tools."""
    print("Installing common development tools...")

    results: list[bool] = []
    results.append(install_git_linux())
    results.append(install_docker_linux())
    results.append(install_nodejs_linux())

    success = all(results)

    if success:
        print("All development tools installed successfully!")
    else:
        print("Some tools may not have been installed correctly.")

    return success
