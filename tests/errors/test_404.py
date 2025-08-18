from typing import Any, Callable

from flask.testing import FlaskClient


def test_returns_404_on_missing_route(
    client: FlaskClient, json_of: Callable[[Any], dict[str, Any]]
) -> None:
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    assert json_of(resp) == {"message": "Not Found"}
