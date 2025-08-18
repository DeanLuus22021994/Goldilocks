def test_returns_404_on_missing_route(client, json_of) -> None:
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    assert json_of(resp) == {"message": "Not Found"}
