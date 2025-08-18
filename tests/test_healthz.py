def test_healthz_status_ok(client) -> None:
    resp = client.get("/healthz")
    assert resp.status_code == 200


def test_healthz_body_ok(client, json_of) -> None:
    resp = client.get("/healthz")
    assert json_of(resp) == {"status": "ok"}


def test_healthz_sets_correlation_header(client, correlation_id_header) -> None:
    resp = client.get("/healthz", headers=correlation_id_header)
    # Echoed back by after_request hook
    assert resp.headers.get("X-Request-ID") == correlation_id_header["X-Request-ID"]
