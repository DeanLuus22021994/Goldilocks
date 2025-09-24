#!/usr/bin/env python3
"""Clean up ALL temporary Python files and caches - CRITICAL CLEANUP.

This script aggressively removes:
- Python bytecode cache (__pycache__ directories)
- Compiled Python files (.pyc, .pyo, .pyd)
- Virtual environments (.venv, venv, env)
- All linter caches (ruff, flake8, pylint, black, isort)
- Type checking cache (mypy, pyright, pylance)
- Testing cache (pytest, coverage, tox)
- IDE cache files (VS Code, PyCharm, etc.)
- Package manager caches (pip, poetry, conda)
- Jupyter notebook checkpoints
- Build and distribution artifacts
- All temporary and swap files

Usage: python clean.py [--force]
Use --force to skip confirmations for destructive operations.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def remove_directory(path: Path, description: str) -> int:
    """Remove directory and return count of items removed."""
    if path.exists() and path.is_dir():
        try:
            shutil.rmtree(path)
            print(f"✅ Removed {description}: {path}")
            return 1
        except OSError as e:
            print(f"❌ Failed to remove {description}: {path} - {e}")
            return 0
    return 0


def remove_file(path: Path, description: str) -> int:
    """Remove file and return count of items removed."""
    if path.exists() and path.is_file():
        try:
            path.unlink()
            print(f"✅ Removed {description}: {path}")
            return 1
        except OSError as e:
            print(f"❌ Failed to remove {description}: {path} - {e}")
            return 0
    return 0


def clean_python_cache() -> int:
    """Clean Python bytecode cache files."""
    count = 0
    root = Path(".")

    print("🧹 Cleaning Python cache files...")

    # Remove __pycache__ directories
    for pycache_dir in root.rglob("__pycache__"):
        count += remove_directory(pycache_dir, "__pycache__ directory")

    # Remove .pyc and .pyo files
    for pyc_file in root.rglob("*.pyc"):
        count += remove_file(pyc_file, "bytecode file")

    for pyo_file in root.rglob("*.pyo"):
        count += remove_file(pyo_file, "optimized bytecode file")

    return count


def clean_test_cache() -> int:
    """Clean test-related cache files."""
    count = 0
    root = Path(".")

    print("🧪 Cleaning test cache files...")

    # Remove pytest cache
    pytest_cache = root / ".pytest_cache"
    count += remove_directory(pytest_cache, "pytest cache")

    # Remove coverage files
    coverage_file = root / ".coverage"
    count += remove_file(coverage_file, "coverage data")

    coverage_xml = root / "coverage.xml"
    count += remove_file(coverage_xml, "coverage XML report")

    htmlcov_dir = root / "htmlcov"
    count += remove_directory(htmlcov_dir, "HTML coverage report")

    return count


def clean_virtual_environments() -> int:
    """Clean virtual environment directories."""
    count = 0
    root = Path(".")

    print("🐍 Cleaning virtual environments...")

    # Common virtual environment directory names
    venv_names = [".venv", "venv", "env", ".env", "virtualenv", ".virtualenv"]

    for venv_name in venv_names:
        venv_path = root / venv_name
        if venv_path.exists() and venv_path.is_dir():
            # Check if it's actually a virtual environment
            if (
                (venv_path / "pyvenv.cfg").exists()
                or (venv_path / "Scripts" / "python.exe").exists()
                or (venv_path / "bin" / "python").exists()
            ):
                count += remove_directory(
                    venv_path, f"virtual environment ({venv_name})"
                )

    return count


def clean_linter_caches() -> int:
    """Clean linter and formatter cache files."""
    count = 0
    root = Path(".")

    print("🔧 Cleaning linter and formatter caches...")

    # Linter and formatter caches
    linter_caches = [
        (".ruff_cache", "Ruff cache"),
        (".flake8_cache", "Flake8 cache"),
        (".pylint_cache", "Pylint cache"),
        (".black_cache", "Black cache"),
        (".isort_cache", "isort cache"),
        (".bandit", "Bandit cache"),
        (".pre-commit", "pre-commit cache"),
    ]

    for cache_dir, description in linter_caches:
        cache_path = root / cache_dir
        count += remove_directory(cache_path, description)

    return count


def clean_type_checking_cache() -> int:
    """Clean type checking cache files."""
    count = 0
    root = Path(".")

    print("🔍 Cleaning type checking cache...")

    # Remove mypy cache
    mypy_cache = root / ".mypy_cache"
    count += remove_directory(mypy_cache, "mypy cache")

    # Remove pyright cache
    pyright_cache = root / ".pyright"
    count += remove_directory(pyright_cache, "pyright cache")

    # Remove pylance cache
    pylance_cache = root / ".pylance"
    count += remove_directory(pylance_cache, "Pylance cache")

    return count


def clean_build_artifacts() -> int:
    """Clean build and distribution artifacts."""
    count = 0
    root = Path(".")

    print("📦 Cleaning build artifacts...")

    # Remove build directories
    build_dir = root / "build"
    count += remove_directory(build_dir, "build directory")

    dist_dir = root / "dist"
    count += remove_directory(dist_dir, "dist directory")

    # Remove egg-info directories
    for egg_info in root.rglob("*.egg-info"):
        count += remove_directory(egg_info, "egg-info directory")

    return count


def clean_package_manager_caches() -> int:
    """Clean package manager caches."""
    count = 0
    root = Path(".")

    print("📦 Cleaning package manager caches...")  # fixed corrupted emoji

    # pip cache (usually in user directory, but check local)
    pip_cache = root / ".pip_cache"
    count += remove_directory(pip_cache, "pip cache")

    # poetry cache
    poetry_cache = root / ".poetry_cache"
    count += remove_directory(poetry_cache, "Poetry cache")

    # conda cache
    conda_cache = root / ".conda"
    count += remove_directory(conda_cache, "Conda cache")

    return count


def clean_ide_files() -> int:
    """Clean IDE-specific temporary files."""
    count = 0
    root = Path(".")

    print("💻 Cleaning IDE temporary files...")

    # VS Code caches and temp files
    vscode_caches = [
        ".vscode/.ropeproject",
        ".vscode/settings.json.bak",
        ".vscode/launch.json.bak",
    ]

    for cache_path in vscode_caches:
        cache_file = root / cache_path
        if cache_file.exists():
            if cache_file.is_dir():
                count += remove_directory(cache_file, "VS Code cache")
            else:
                count += remove_file(cache_file, "VS Code backup file")

    # PyCharm project files (.idea)
    for idea_dir in root.rglob(".idea"):
        if idea_dir.is_dir():
            count += remove_directory(idea_dir, "PyCharm .idea directory")

    # Remove Python language server cache
    pylsp_cache = root / ".pylsp"
    count += remove_directory(pylsp_cache, "Python LSP cache")

    # Remove rope project cache
    rope_cache = root / ".ropeproject"
    count += remove_directory(rope_cache, "Rope project cache")

    return count


def clean_temporary_files() -> int:
    """Clean temporary and swap files."""
    count = 0
    root = Path(".")

    print("🗑️  Cleaning temporary files...")

    # Remove common temporary file patterns
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*.bak",
        "*.swp",
        "*.swo",
        "*~",
        ".DS_Store",
        "Thumbs.db",
        "desktop.ini",
    ]

    for pattern in temp_patterns:
        for temp_file in root.rglob(pattern):
            if temp_file.is_file():
                count += remove_file(temp_file, f"temporary file ({pattern})")

    return count


def clean_jupyter_files() -> int:
    """Clean Jupyter notebook checkpoints and temporary files."""
    count = 0
    root = Path(".")

    print("📓 Cleaning Jupyter files...")

    # Remove Jupyter checkpoints
    for checkpoint_dir in root.rglob(".ipynb_checkpoints"):
        count += remove_directory(checkpoint_dir, "Jupyter checkpoint")

    # Remove Jupyter lab workspaces
    jupyter_lab_dir = root / ".jupyter"
    count += remove_directory(jupyter_lab_dir, "Jupyter lab workspace")

    return count


def _confirm(action: str, force: bool) -> bool:
    """Ask for confirmation unless force is True."""
    if force:
        return True
    try:
        reply = input(f"{action} Proceed? [y/N]: ").strip().lower()
        return reply in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print("\n⚠️  Operation cancelled.")
        return False


def main() -> None:
    """Main cleanup function."""
    parser = argparse.ArgumentParser(
        description="Aggressively clean Python caches and temp files."
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Skip confirmations for destructive operations",
    )
    args = parser.parse_args()

    print("🚀 Starting Python environment cleanup...")
    print(f"📁 Working directory: {os.getcwd()}")
    print()

    total_removed = 0

    try:
        # Core safe cleanups
        total_removed += clean_python_cache()
        total_removed += clean_test_cache()
        total_removed += clean_linter_caches()
        total_removed += clean_type_checking_cache()
        total_removed += clean_build_artifacts()
        total_removed += clean_ide_files()
        total_removed += clean_temporary_files()
        total_removed += clean_jupyter_files()

        # Destructive operations (confirmation-gated)
        if _confirm("🐍 Remove detected virtual environments.", args.force):
            total_removed += clean_virtual_environments()
        else:
            print("⏭️  Skipped virtual environments.")

        if _confirm(
            "📦 Remove local package manager caches (pip/poetry/conda).",
            args.force,
        ):
            total_removed += clean_package_manager_caches()
        else:
            print("⏭️  Skipped package manager caches.")

        print()
        print("🎉 Cleanup completed successfully!")
        print(f"📊 Total items removed: {total_removed}")

        if total_removed == 0:
            print("✨ Environment was already clean!")
        else:
            print("💡 You can now run your tools to see actual errors.")

    except KeyboardInterrupt:
        print("\n⚠️  Cleanup interrupted by user")
        sys.exit(1)
    except OSError as e:
        print(f"\n❌ Cleanup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
