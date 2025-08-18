def test_404_json_message(client, json_of):
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    assert json_of(resp) == {"message": "Not Found"}
