"""
Linux package management utilities.

Handles system package installation and management on Linux distributions.
Follows MODERNIZE and HIGH COMPATIBILITY principles.
"""

import subprocess

from ..common import run_command

__version__ = "1.0.0"


def detect_package_manager() -> str:
    """Detect the available package manager on the system."""
    managers = {
        "apt": ["apt", "--version"],
        "yum": ["yum", "--version"],
        "dnf": ["dnf", "--version"],
        "pacman": ["pacman", "--version"],
        "zypper": ["zypper", "--version"],
    }

    for manager, test_cmd in managers.items():
        try:
            result = subprocess.run(test_cmd, capture_output=True, timeout=5)
            if result.returncode == 0:
                return manager
        except Exception:
            continue

    return "unknown"


def update_package_list() -> bool:
    """Update the package manager's package list."""
    manager = detect_package_manager()

    update_commands = {
        "apt": ["sudo", "apt", "update"],
        "yum": ["sudo", "yum", "check-update"],
        "dnf": ["sudo", "dnf", "check-update"],
        "pacman": ["sudo", "pacman", "-Sy"],
        "zypper": ["sudo", "zypper", "refresh"],
    }

    if manager in update_commands:
        print(f"Updating package list using {manager}...")
        return_code, _, _ = run_command(update_commands[manager])
        return return_code == 0
    else:
        print(f"Unknown package manager: {manager}")
        return False


def install_system_packages(packages: list[str]) -> bool:
    """Install system packages using the detected package manager."""
    manager = detect_package_manager()

    install_commands = {
        "apt": ["sudo", "apt", "install", "-y"] + packages,
        "yum": ["sudo", "yum", "install", "-y"] + packages,
        "dnf": ["sudo", "dnf", "install", "-y"] + packages,
        "pacman": ["sudo", "pacman", "-S", "--noconfirm"] + packages,
        "zypper": ["sudo", "zypper", "install", "-y"] + packages,
    }

    if manager in install_commands:
        print(f"Installing packages using {manager}: {' '.join(packages)}")
        return_code, _, _ = run_command(install_commands[manager])
        return return_code == 0
    else:
        print(f"Unknown package manager: {manager}")
        return False


def check_package_installed(package: str) -> bool:
    """Check if a system package is installed."""
    manager = detect_package_manager()

    check_commands = {
        "apt": ["dpkg", "-l", package],
        "yum": ["rpm", "-q", package],
        "dnf": ["rpm", "-q", package],
        "pacman": ["pacman", "-Q", package],
        "zypper": ["rpm", "-q", package],
    }

    if manager in check_commands:
        try:
            result = subprocess.run(check_commands[manager], capture_output=True, timeout=10)
            return result.returncode == 0
        except Exception:
            return False

    return False


def get_development_packages() -> dict[str, list[str]]:
    """Get development packages for different package managers."""
    return {
        "apt": [
            "build-essential",
            "python3-dev",
            "python3-pip",
            "python3-venv",
            "git",
            "curl",
            "wget",
            "software-properties-common",
            "apt-transport-https",
            "ca-certificates",
            "gnupg",
            "lsb-release",
        ],
        "yum": [
            "gcc",
            "gcc-c++",
            "make",
            "python3-devel",
            "python3-pip",
            "git",
            "curl",
            "wget",
            "which",
            "tar",
            "gzip",
        ],
        "dnf": [
            "gcc",
            "gcc-c++",
            "make",
            "python3-devel",
            "python3-pip",
            "git",
            "curl",
            "wget",
            "which",
            "tar",
            "gzip",
        ],
        "pacman": [
            "base-devel",
            "python",
            "python-pip",
            "git",
            "curl",
            "wget",
            "which",
            "tar",
            "gzip",
        ],
        "zypper": [
            "gcc",
            "gcc-c++",
            "make",
            "python3-devel",
            "python3-pip",
            "git",
            "curl",
            "wget",
            "which",
            "tar",
            "gzip",
        ],
    }


def install_development_environment() -> bool:
    """Install essential development packages."""
    manager = detect_package_manager()
    dev_packages = get_development_packages()

    if manager not in dev_packages:
        print(f"Development packages not defined for {manager}")
        return False

    # Update package list first
    if not update_package_list():
        print("Warning: Failed to update package list")

    # Install development packages
    packages = dev_packages[manager]
    return install_system_packages(packages)
