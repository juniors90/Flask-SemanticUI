def test_sample_request(app, client):
    @app.get("/sample")
    def sample():
        return "OK"

    r = client.get("/sample")
    assert r.status_code == 200
    assert r.data == b"OK"
