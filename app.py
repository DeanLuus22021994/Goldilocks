"""Compatibility shim for tests and tooling expecting `app.py` at repo root.

This module re-exports the Flask `app` instance and the `pkg_version` symbol
from the package path `goldilocks.app` so legacy imports keep working (for
example, tests that do `from app import app` or reference `app.pkg_version`).
"""

from __future__ import annotations

import os
import sys

# Ensure `src/` is on sys.path so `goldilocks` package is importable in dev/tests
_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from goldilocks.app import app, pkg_version  # noqa: E402,F401

__all__ = ["app", "pkg_version"]
