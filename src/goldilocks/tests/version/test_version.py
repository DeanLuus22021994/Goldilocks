from collections.abc import Callable
from typing import Any

from flask.testing import FlaskClient


def test_version_response_includes_expected_keys(client: FlaskClient, json_of: Callable[[Any], Any]) -> None:
    resp = client.get("/version")
    assert resp.status_code == 200
    data = json_of(resp)
    assert {"app", "python", "flask", "platform"}.issubset(data.keys())
