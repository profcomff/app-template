import pytest


@pytest.mark.authenticated()
def test_whoami(client):
    resp = client.get("/example/whoami")
    assert resp.status_code == 200
    assert resp.json()["id"] == 0


@pytest.mark.authenticated()
def test_touch(client):
    resp = client.post("/example/touch")
    assert resp.status_code == 200
    assert resp.json()["id"] == 0
    assert resp.json()["count"] == 1

    resp = client.post("/example/touch")
    assert resp.status_code == 200
    assert resp.json()["id"] == 0
    assert resp.json()["count"] == 2
