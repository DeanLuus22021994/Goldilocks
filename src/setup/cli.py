#!/usr/bin/env python3
"""
Goldilocks Environment Setup CLI

Cross-platform command-line utility for setting up the Goldilocks
development environment on Windows, Linux, and container environments.
"""

import argparse
import sys
from typing import Any


def main():
    """Main entry point for the setup CLI."""
    parser = argparse.ArgumentParser(
        description="Goldilocks Environment Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_cli.py                    # Auto-detect and setup environment
  python setup_cli.py --platform linux  # Force Linux setup
  python setup_cli.py --verify           # Verify current environment
  python setup_cli.py --interactive      # Interactive setup
        """,
    )

    parser.add_argument(
        "--platform",
        choices=["windows", "linux", "container", "auto"],
        default="auto",
        help="Force a specific platform setup (default: auto-detect)",
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify environment instead of setting up",
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode with prompts",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument(
        "--development",
        action="store_true",
        help="Setup development environment with additional tools",
    )

    parser.add_argument(
        "--no-packages",
        action="store_true",
        help="Skip Python package installation",
    )

    parser.add_argument("--no-git", action="store_true", help="Skip Git installation")

    parser.add_argument("--no-docker", action="store_true", help="Skip Docker installation")

    args = parser.parse_args()

    # Print banner
    print("=" * 60)
    print("GOLDILOCKS ENVIRONMENT SETUP")
    print("=" * 60)

    try:
        # Import setup modules
        from setup import (
            get_platform_info,
            setup_environment,
            verify_environment,
        )

        # Get platform information
        platform_info = get_platform_info()
        print(f"Detected platform: {platform_info['system']}")
        print(f"Python version: {platform_info['python_version']}")

        if args.verbose:
            print(f"Machine: {platform_info.get('machine', 'unknown')}")
            print(f"Architecture: {platform_info.get('architecture', 'unknown')}")
            if platform_info.get("is_container"):
                print("Container environment detected")
            if platform_info.get("is_wsl"):
                print("WSL environment detected")

        # Handle verification mode
        if args.verify:
            print("\nVerifying environment...")
            results = verify_environment()

            print("\nVerification Results:")
            print("-" * 40)

            all_good = True
            for component, status in results.items():
                status_symbol = "✓" if status else "✗"
                print(f"{status_symbol} {component}: {'OK' if status else 'MISSING'}")
                if not status:
                    all_good = False

            if all_good:
                print("\n✓ All components are properly installed!")
                return 0
            else:
                print("\n✗ Some components are missing or not properly configured.")
                print("Run without --verify to install missing components.")
                return 1

        # Prepare configuration
        config: dict[str, Any] = {
            "interactive": args.interactive,
            "verbose": args.verbose,
            "development": args.development,
            "skip_packages": args.no_packages,
            "skip_git": args.no_git,
            "skip_docker": args.no_docker,
        }

        # Handle interactive mode
        if args.interactive:
            print("\nInteractive setup mode enabled.")
            config.update(_interactive_config())

        # Override platform if specified
        if args.platform != "auto":
            print(f"Forcing platform: {args.platform}")
            # This would require modifying the setup modules to accept platform override

        print("\nStarting environment setup...")
        print("-" * 40)

        # Run setup
        success = setup_environment(config)

        print("\n" + "=" * 60)
        if success:
            print("SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("Goldilocks is ready to use.")
            print("\nNext steps:")
            print("1. Navigate to your project directory")
            print("2. Run 'python app.py' to start the application")
            print("3. Visit http://localhost:9000 in your browser")

            # Optionally run verification
            if not args.no_packages:
                print("\nRunning verification...")
                verify_results = verify_environment()
                failed_components = [k for k, v in verify_results.items() if not v]
                if failed_components:
                    print(f"Warning: Some components may still have issues: {failed_components}")

            return 0
        else:
            print("SETUP COMPLETED WITH ISSUES")
            print("=" * 60)
            print("Some components may not be properly configured.")
            print("Check the output above for any error messages.")
            return 1

    except ImportError as e:
        print(f"Error: Could not import setup modules: {e}")
        print("Make sure you're running this from the correct directory.")
        return 1
    except KeyboardInterrupt:
        print("\nSetup interrupted by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def _interactive_config() -> dict[str, Any]:
    """Gather configuration in interactive mode."""
    config: dict[str, Any] = {}

    print("\nInteractive Configuration:")
    print("Press Enter to use default values in [brackets]")

    # Ask about development tools
    dev_tools = input("Install development tools (pytest, black, mypy)? [Y/n]: ").strip().lower()
    config["development"] = dev_tools != "n"

    # Ask about Git
    install_git = input("Install Git? [Y/n]: ").strip().lower()
    config["skip_git"] = install_git == "n"

    # Ask about Docker
    install_docker = input("Install Docker? [Y/n]: ").strip().lower()
    config["skip_docker"] = install_docker == "n"

    # Ask about verbosity
    verbose = input("Enable verbose output? [Y/n]: ").strip().lower()
    config["verbose"] = verbose != "n"

    return config


if __name__ == "__main__":
    sys.exit(main())
