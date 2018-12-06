def test_root(client):
    """ Test that server is up """
    resp = client.get('/api/')
    assert resp.status_code == 200
