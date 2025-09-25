#!/usr/bin/env python3
"""
Documentation generation entry point.

This script provides backward compatibility while using the new
modular documentation package.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from docs.cli import main  # noqa: E402

if __name__ == '__main__':
    sys.exit(main())
