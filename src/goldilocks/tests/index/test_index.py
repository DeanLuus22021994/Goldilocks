"""Tests for the index endpoint ensuring HTML response and required headers."""

from __future__ import annotations

from flask.testing import FlaskClient


def test_index_serves_html_and_headers(
    client: FlaskClient,
    correlation_id_header: dict[str, str],
) -> None:
    """Ensure index serves HTML and sets timing and correlation headers."""
    res = client.get("/", headers=correlation_id_header)
    assert res.status_code == 200
    ctype = res.headers.get("Content-Type", "")
    assert ctype.startswith("text/html")

    # timing and correlation headers
    expected_id = correlation_id_header["X-Request-ID"]
    assert res.headers.get("X-Request-ID") == expected_id
    assert "X-Response-Time-ms" in res.headers
    # basic sanity that it's a float string
    float(res.headers["X-Response-Time-ms"])  # conversion should succeed
