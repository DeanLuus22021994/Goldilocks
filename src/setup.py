"""
Setup configuration for the Goldilocks package.

This allows the entire Goldilocks application to be installed and compiled
with environment-specific setup utilities following modern Python practices.
Includes cross-platform installation support for Windows, Linux, and containers.
"""

from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""


class PostInstallCommand(install):
    """Post-installation command to setup environment-specific requirements."""

    def run(self):
        """Run the standard installation and then setup environment."""
        install.run(self)
        self._post_install()

    def _post_install(self):
        """Run post-installation setup."""
        try:
            # Import setup module after installation
            from setup import get_platform_info, setup_environment

            print("=" * 60)
            print("GOLDILOCKS POST-INSTALLATION SETUP")
            print("=" * 60)

            # Get platform information
            platform_info = get_platform_info()
            print(f"Detected platform: {platform_info['system']}")
            print(f"Python version: {platform_info['python_version']}")
            print(f"Architecture: {platform_info.get('machine', 'unknown')}")

            if platform_info.get("is_container"):
                print("Container environment detected")
            if platform_info.get("is_wsl"):
                print("WSL environment detected")

            print("\nStarting environment setup...")

            # Run environment setup
            config = {
                "interactive": False,  # Non-interactive installation
                "verbose": True,
            }

            success = setup_environment(config)

            if success:
                print("\n" + "=" * 60)
                print("SETUP COMPLETED SUCCESSFULLY!")
                print("=" * 60)
                print("Goldilocks is ready to use.")
                print("\nNext steps:")
                print("1. Navigate to your project directory")
                print("2. Run 'python app.py' to start the application")
                print("3. Visit http://localhost:9000 in your browser")
            else:
                print("\n" + "=" * 60)
                print("SETUP COMPLETED WITH ISSUES")
                print("=" * 60)
                print("Some components may not be properly configured.")
                print("Check the output above for any error messages.")
                print("You may need to install some dependencies manually.")

        except ImportError as e:
            print(f"Warning: Could not run post-installation setup: {e}")
            print("You may need to run the setup manually using:")
            print("  python -c 'from setup import setup_environment; setup_environment()'")
        except Exception as e:
            print(f"Error during post-installation setup: {e}")


class PostDevelopCommand(develop):
    """Post-development command to setup environment-specific requirements."""

    def run(self):
        """Run the standard development installation and then setup environment."""
        develop.run(self)
        self._post_install()

    def _post_install(self):
        """Run post-installation setup for development."""
        try:
            from setup import get_platform_info, setup_environment

            print("=" * 60)
            print("GOLDILOCKS DEVELOPMENT SETUP")
            print("=" * 60)

            platform_info = get_platform_info()
            print(f"Setting up development environment for {platform_info['system']}")

            # Run environment setup with development configuration
            config = {
                "interactive": False,
                "verbose": True,
                "development": True,
            }

            success = setup_environment(config)

            if success:
                print("\nDevelopment environment setup completed!")
            else:
                print("\nDevelopment environment setup completed with issues.")

        except Exception as e:
            print(f"Error during development setup: {e}")


setup(
    name="goldilocks",
    version="2.0.0",
    description="Modern Flask application with cross-platform setup utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Goldilocks Team",
    author_email="team@goldilocks.dev",
    url="https://github.com/DeanLuus22021994/Goldilocks",
    packages=find_packages(where="."),
    package_dir={"": "."},
    python_requires=">=3.9",
    install_requires=[
        # Core web framework
        "flask>=3.1.0",
        "flask-sqlalchemy>=3.1.0",
        "flask-login>=0.6.0",
        "flask-wtf>=1.2.0",
        # Database
        "sqlalchemy>=2.0.0",
        "pymysql>=1.1.0",
        # Forms and validation
        "wtforms>=3.1.0",
        "bcrypt>=4.1.0",
        # Configuration and utilities
        "python-dotenv>=1.0.0",
        # Documentation generation
        "markitdown>=0.0.1a2",
        # HTTP client for health checks
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.8.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=8.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.12.0",
            "coverage>=7.0.0",
        ],
        "docs": [
            "markitdown>=0.0.1a2",
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "goldilocks=goldilocks.app:main",
            "goldilocks-setup=setup:setup_environment",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="flask web application cross-platform setup automation docker",
    project_urls={
        "Bug Reports": "https://github.com/DeanLuus22021994/Goldilocks/issues",
        "Source": "https://github.com/DeanLuus22021994/Goldilocks",
        "Documentation": "https://github.com/DeanLuus22021994/Goldilocks/tree/main/docs",
        "Changelog": "https://github.com/DeanLuus22021994/Goldilocks/blob/main/CHANGELOG.md",
    },
    include_package_data=True,
    package_data={
        "goldilocks": ["templates/**/*", "static/**/*"],
        "setup": ["**/*.py"],
    },
    zip_safe=False,
)
