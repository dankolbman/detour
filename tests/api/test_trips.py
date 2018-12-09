from detour.api.models import Trip


def test_get(client, db):
    """ Test that points can be retrieved """
    resp = client.get('/api/trips')
    assert resp.status_code == 200


def test_create(client, user, db):
    """ Test that trips can be added """
    trip = {
        'owner': user.id,
        'name': 'test',
        'description': 'lorem ipsum'
    }
    resp = client.post('/api/trips', trip)

    assert resp.status_code == 201
    assert Trip.objects.count() == 1

    resp = client.get(f'/api/trips/{resp.json()["id"]}')
    assert resp.json()['owner'] == user.id


def test_create_with_points(client, trip, db):
    """ Test format with points """
    point = {
        'lat': 0.123,
        'lon': 1.32,
        'trip': trip.id
    }
    resp = client.post(f'/api/trips/{trip.id}/points', point)
    assert resp.status_code == 201
    assert Trip.objects.count() == 1

    resp = client.get(f'/api/trips/{trip.id}')
    assert resp.json()['points'].endswith(f'/api/trips/{trip.id}/points')
