"""
Container health check utilities for Goldilocks.

Handles container readiness and liveness checks,
service verification and monitoring utilities.
Follows LIGHTWEIGHT and SEPARATION OF CONCERNS principles.
"""

import subprocess
import sys
from pathlib import Path

__version__ = "1.0.0"


def check_python_environment() -> bool:
    """Check if Python environment is properly configured."""
    try:
        # Check Python version
        version_info = sys.version_info
        if version_info.major != 3 or version_info.minor < 12:
            print(f"Warning: Python {version_info.major}.{version_info.minor} may not be optimal")

        # Check if pip is available
        result = subprocess.run(
            ["python", "-m", "pip", "--version"],
            capture_output=True,
            timeout=10,
        )

        if result.returncode != 0:
            print("Error: pip is not available")
            return False

        print("Python environment check passed")
        return True

    except Exception as e:
        print(f"Python environment check failed: {e}")
        return False


def check_required_packages() -> bool:
    """Check if all required packages are installed."""
    required_packages = [
        "flask",
        "sqlalchemy",
        "pymysql",
        "python-dotenv",
        "wtforms",
        "flask-wtf",
        "flask-login",
        "flask-sqlalchemy",
        "bcrypt",
    ]

    missing_packages: list[str] = []

    for package in required_packages:
        try:
            # Try to import the package
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        return False

    print("All required packages are available")
    return True


def check_file_permissions() -> bool:
    """Check if file permissions are properly set."""
    try:
        # Check if current directory is writable
        test_file = Path("test_write_permissions.tmp")
        test_file.write_text("test")
        test_file.unlink()

        # Check if application files exist
        app_files = ["app.py", "requirements.txt"]
        missing_files = [f for f in app_files if not Path(f).exists()]

        if missing_files:
            print(f"Missing application files: {', '.join(missing_files)}")
            return False

        print("File permissions check passed")
        return True

    except Exception as e:
        print(f"File permissions check failed: {e}")
        return False


def check_network_connectivity() -> bool:
    """Check basic network connectivity."""
    try:
        # Simple connectivity check using ping
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("Network connectivity check passed")
            return True
        else:
            print("Network connectivity check failed")
            return False

    except Exception as e:
        print(f"Network connectivity check failed: {e}")
        return False


def check_application_startup() -> bool:
    """Check if the application can start properly."""
    try:
        # Try to import the main application module
        import importlib.util

        # Check if app.py exists
        if not Path("app.py").exists():
            print("Application file 'app.py' not found")
            return False

        # Try to load the module
        spec = importlib.util.spec_from_file_location("app", "app.py")
        if spec and spec.loader:
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)
            print("Application startup check passed")
            return True
        else:
            print("Failed to load application module")
            return False

    except Exception as e:
        print(f"Application startup check failed: {e}")
        return False


def run_health_checks() -> dict[str, bool]:
    """Run all health checks and return results."""
    print("Running container health checks...")

    checks = {
        "python_environment": check_python_environment(),
        "required_packages": check_required_packages(),
        "file_permissions": check_file_permissions(),
        "network_connectivity": check_network_connectivity(),
        "application_startup": check_application_startup(),
    }

    passed = sum(checks.values())
    total = len(checks)

    print(f"\nHealth check results: {passed}/{total} passed")

    for check_name, result in checks.items():
        status = "PASS" if result else "FAIL"
        print(f"  {check_name}: {status}")

    return checks


def is_container_ready() -> bool:
    """Check if container is ready to serve requests."""
    checks = run_health_checks()

    # Container is ready if all critical checks pass
    critical_checks = [
        "python_environment",
        "required_packages",
        "file_permissions",
        "application_startup",
    ]

    for check_name in critical_checks:
        if not checks.get(check_name, False):
            print(f"Container not ready: {check_name} failed")
            return False

    print("Container is ready!")
    return True
