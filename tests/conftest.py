import json
import os
import sys
from typing import Any, Callable

import pytest

# Ensure project root is importable so `import app` resolves to app.py at repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app as flask_app  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """Return the Flask app instance once per test session."""
    return flask_app


@pytest.fixture()
def client(app):
    """Lightweight test client per test for isolation."""
    return app.test_client()


@pytest.fixture()
def json_of() -> Callable[[Any], dict[str, Any]]:
    """Decode a Flask response body to JSON."""

    def _json(resp: Any) -> dict[str, Any]:
        return json.loads(resp.data.decode("utf-8"))

    return _json


@pytest.fixture()
def correlation_id_header() -> dict[str, str]:
    """Provide a stable correlation ID header for tests."""
    return {"X-Request-ID": "test-cid-123"}
