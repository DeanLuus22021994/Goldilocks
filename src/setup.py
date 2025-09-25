"""
Setup configuration for the docs package.

This allows the docs package to be installed and compiled
as a standalone package following modern Python practices.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = (
    readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
)

setup(
    name="goldilocks-docs",
    version="0.1.0",
    description="Modern documentation generation system for Goldilocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Goldilocks Team",
    author_email="team@goldilocks.dev",
    url="https://github.com/DeanLuus22021994/Goldilocks",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "markitdown>=0.0.1a2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "goldilocks-docs=docs.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    keywords="documentation generation markdown automation",
    project_urls={
        "Bug Reports": "https://github.com/DeanLuus22021994/Goldilocks/issues",
        "Source": "https://github.com/DeanLuus22021994/Goldilocks",
        "Documentation": "https://github.com/DeanLuus22021994/Goldilocks"
        "/tree/main/docs",
    },
)
