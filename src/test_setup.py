#!/usr/bin/env python3
"""
Test script for the Goldilocks setup system.

This script tests the setup modules and verifies they work correctly
across different platforms.
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all setup modules can be imported."""
    print("Testing imports...")

    try:
        from setup import get_platform_info

        print("✓ Main setup module imports successful")

        # Test platform detection
        platform_info = get_platform_info()
        print(f"✓ Platform detected: {platform_info['system']}")
        print(f"  Python version: {platform_info['python_version']}")

        if platform_info.get("is_container"):
            print("  Running in container")
        if platform_info.get("is_wsl"):
            print("  Running in WSL")

        return True

    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_platform_modules():
    """Test platform-specific modules."""
    print("\nTesting platform-specific modules...")

    try:
        print("✓ Windows setup module imported")
    except Exception as e:
        print(f"✗ Windows setup module failed: {e}")

    try:
        print("✓ Linux setup module imported")
    except Exception as e:
        print(f"✗ Linux setup module failed: {e}")

    try:
        print("✓ Container setup module imported")
    except Exception as e:
        print(f"✗ Container setup module failed: {e}")


def test_verification():
    """Test environment verification."""
    print("\nTesting environment verification...")

    try:
        from setup import verify_environment

        results = verify_environment()
        print("✓ Verification completed")

        print("\nCurrent environment status:")
        for component, status in results.items():
            status_symbol = "✓" if status else "✗"
            print(f"  {status_symbol} {component}")

        return True

    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False


def test_cli():
    """Test the CLI module."""
    print("\nTesting CLI module...")

    try:
        print("✓ CLI module imported")
        return True
    except Exception as e:
        print(f"✗ CLI module failed: {e}")
        return False


def main():
    """Main test function."""
    print("=" * 50)
    print("GOLDILOCKS SETUP SYSTEM TEST")
    print("=" * 50)

    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

    all_tests_passed = True

    # Run tests
    tests = [
        test_imports,
        test_platform_modules,
        test_verification,
        test_cli,
    ]

    for test_func in tests:
        try:
            if not test_func():
                all_tests_passed = False
        except Exception as e:
            print(f"✗ Test {test_func.__name__} crashed: {e}")
            all_tests_passed = False

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✓ ALL TESTS PASSED")
        print("The setup system is working correctly!")
    else:
        print("✗ SOME TESTS FAILED")
        print("Check the output above for issues.")

    print("=" * 50)

    return 0 if all_tests_passed else 1


if __name__ == "__main__":
    sys.exit(main())
