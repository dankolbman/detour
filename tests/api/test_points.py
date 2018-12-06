from detour.api.models import Point


def test_get(client, db):
    """ Test that points can be retrieved """
    resp = client.get('/api/points')
    assert resp.status_code == 200


def test_create(client, db):
    """ Test that points can be added """
    point = {
        'lat': 0.123,
        'lon': 1.32,
    }
    resp = client.post('/api/points', point)
    assert resp.status_code == 201
    assert Point.objects.count() == 1

    resp = client.get(f'/api/points/{resp.json()["id"]}')
    assert resp.json()['lat'] == 0.123
    assert resp.json()['lon'] == 1.32
