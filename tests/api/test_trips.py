from detour.api.models import Trip, Point


def test_get(admin_client, db):
    """ Test that points can be retrieved """
    resp = admin_client.get('/api/trips')
    assert resp.status_code == 200


def test_create(admin_client, user, db):
    """ Test that trips can be added """
    trip = {
        'owner': user.id,
        'name': 'test',
        'description': 'lorem ipsum'
    }
    resp = admin_client.post('/api/trips', trip)

    assert resp.status_code == 201
    assert Trip.objects.count() == 1

    resp = admin_client.get(f'/api/trips/{resp.json()["id"]}')
    assert resp.json()['owner'] == user.id


def test_create_with_points(admin_client, trip, db):
    """ Test format with points """
    point = {
        'lat': 0.123,
        'lon': 1.32,
        'trip': trip.id,
        'time': '2019-01-01T00:00',
    }
    resp = admin_client.post(f'/api/trips/{trip.id}/points', point)
    assert resp.status_code == 201
    assert Trip.objects.count() == 1

    resp = admin_client.get(f'/api/trips/{trip.id}')
    assert resp.json()['points'].endswith(f'/api/trips/{trip.id}/points')


def test_filter(client, trip, db):
    """ Test that annotations may be filtered """
    point = {
        'lat': 0.123,
        'lon': 1.32,
        'trip': trip,
        'time': '2019-01-01T00:00',
        'annotation': 'this is a point'
    }
    p = Point.objects.create(**point)
    p.save()

    point['annotation'] = 'new annotation with keyword'
    point['lat'] = 2.00
    p = Point.objects.create(**point)
    p.save()

    resp = client.get(f'/api/trips/{trip.id}/points?search=keyword')
    assert resp.status_code == 200
    assert resp.json()['count'] == 1
    assert resp.json()['results'][0]['annotation'] == point['annotation']


def test_linestring(admin_client, trip, db):
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
        resp = admin_client.post(f'/api/trips/{trip.id}/points', point)

    resp = admin_client.get(f'/api/trips/{trip.id}/linestring')
    assert resp.status_code == 200
    assert resp.json()['type'] == 'LineString'
    assert len(resp.json()['coordinates']) == 20
