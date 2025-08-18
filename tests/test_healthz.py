import json

from app import app


def test_healthz_ok():
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data == {"status": "ok"}