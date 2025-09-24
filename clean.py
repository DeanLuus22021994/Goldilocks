#!/usr/bin/env python3
"""Clean up temporary Python files and caches.

This script safely removes:
- Python bytecode cache (__pycache__ directories)
- Compiled Python files (.pyc, .pyo)
- Pytest cache
- Coverage data files
- Type checking cache (mypy)
- IDE cache files
- Temporary test files

Usage: python clean.py
"""

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
        except Exception as e:
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
        except Exception as e:
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


def clean_ide_files() -> int:
    """Clean IDE-specific temporary files."""
    count = 0
    root = Path(".")
    
    print("💻 Cleaning IDE temporary files...")
    
    # VS Code settings that might cause issues (but keep main settings)
    vscode_dir = root / ".vscode"
    if vscode_dir.exists():
        # Only remove specific cache/temp files, not all .vscode
        for temp_file in ["*.log", "*.tmp"]:
            for file_path in vscode_dir.rglob(temp_file):
                count += remove_file(file_path, "VS Code temp file")
    
    # Remove Python language server cache
    pylsp_cache = root / ".pylsp"
    count += remove_directory(pylsp_cache, "Python LSP cache")
    
    return count


def clean_temporary_files() -> int:
    """Clean various temporary files."""
    count = 0
    root = Path(".")
    
    print("🗂️  Cleaning temporary files...")
    
    # Remove common temp files
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*~",
        ".DS_Store",
        "Thumbs.db",
        "*.swp",
        "*.swo",
        ".vscode-profile-*"
    ]
    
    for pattern in temp_patterns:
        for temp_file in root.rglob(pattern):
            if temp_file.is_file():  # Only remove files, not directories
                count += remove_file(temp_file, f"temporary file ({pattern})")
    
    return count


def main() -> None:
    """Main cleanup function."""
    print("🚀 Starting Python environment cleanup...")
    print(f"📁 Working directory: {os.getcwd()}")
    print()
    
    total_removed = 0
    
    try:
        # Run all cleanup functions
        total_removed += clean_python_cache()
        total_removed += clean_test_cache()
        total_removed += clean_type_checking_cache()
        total_removed += clean_build_artifacts()
        total_removed += clean_ide_files()
        total_removed += clean_temporary_files()
        
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
    except Exception as e:
        print(f"\n❌ Cleanup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()