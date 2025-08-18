import json
import os
import sys
from typing import Callable, Dict

import pytest

# Ensure project root is importable so `import app` resolves to app.py at repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app as flask_app  # noqa: E402


@pytest.fixture(scope="session")
def app():
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def json_of() -> Callable:
    def _json(resp) -> Dict:
        return json.loads(resp.data.decode("utf-8"))

    return _json


@pytest.fixture()
def correlation_id_header() -> Dict[str, str]:
    return {"X-Request-ID": "test-cid-123"}
