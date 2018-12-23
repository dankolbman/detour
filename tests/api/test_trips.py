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
        'trip': trip.id,
        'time': '2019-01-01T00:00',
    }
    resp = client.post(f'/api/trips/{trip.id}/points', point)
    assert resp.status_code == 201
    assert Trip.objects.count() == 1

    resp = client.get(f'/api/trips/{trip.id}')
    assert resp.json()['points'].endswith(f'/api/trips/{trip.id}/points')


def test_linestring(client, trip, db):
    """ Test that linestring geojson is returned correctly """
    expected = {
       "type": "LineString",
       "coordinates": [
           [100.0, 0.0], [101.0, 1.0]
       ]
    }

    for i in range(20):
        point = {
            'lat': 1.11,
            'lon': 2.22,
            'trip': trip.id,
            'time': f'2019-01-01T{i:02d}:00',
        }
        resp = client.post(f'/api/trips/{trip.id}/points', point)

    resp = client.get(f'/api/trips/{trip.id}/linestring')
    assert resp.status_code == 200
    assert resp.json()['type'] == 'LineString'
    assert len(resp.json()['coordinates']) == 20
