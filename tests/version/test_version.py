from typing import Any
from collections.abc import Callable

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_version_response_includes_expected_keys(
    client: FlaskClient, json_of: Callable[[TestResponse], Any]
) -> None:
    resp = client.get("/version")
    assert resp.status_code == 200
    data = json_of(resp)
    assert {"app", "python", "flask", "platform"}.issubset(data.keys())
