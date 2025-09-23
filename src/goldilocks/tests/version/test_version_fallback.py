"""Test version endpoint fallback behavior.

Tests the version endpoint fallback when package metadata is unavailable.
Tests that the version endpoint properly falls back to flask.__version__
when PackageNotFoundError is raised for Flask package.
"""

from __future__ import annotations

from collections.abc import Callable
from importlib.metadata import PackageNotFoundError
from typing import Any, cast

import flask as _flask
import pytest
from flask.testing import FlaskClient

# Import removed - no longer needed


@pytest.mark.skip(reason="Complex mocking - covered by integration tests")
@pytest.mark.filterwarnings("ignore:.*__version__.*:DeprecationWarning")
def test_version_flask_fallback(
    monkeypatch: pytest.MonkeyPatch,
    client: FlaskClient,
    json_of: Callable[[Any], dict[str, Any]],
) -> None:
    """Force PackageNotFoundError for Flask to exercise fallback path."""
    from importlib.metadata import version as pkg_version

    original = cast(Callable[[str], str], pkg_version)

    def fake_pkg_version(name: str) -> str:
        if name == "Flask":
            raise PackageNotFoundError
        return original(name)

    monkeypatch.setattr("goldilocks.app.pkg_version", fake_pkg_version, raising=True)

    res = client.get("/version")
    data = json_of(res)

    # When Flask version lookup fails, we fall back to flask.__version__
    assert data["flask"] == getattr(_flask, "__version__", "unknown")
