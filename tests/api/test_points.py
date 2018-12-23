import datetime
from detour.api.models import Point


def test_get(admin_client, trip, db):
    """ Test that points can be retrieved """
    resp = admin_client.get(f'/api/trips/{trip.id}/points')
    assert resp.status_code == 200


def test_create(admin_client, trip, db):
    """ Test that points can be added """
    point = {
        'time': datetime.datetime.now().isoformat(),
        'lat': 0.123,
        'lon': 1.32,
        'trip': trip.id
    }
    resp = admin_client.post(f'/api/trips/{trip.id}/points', point)

    assert resp.status_code == 201
    assert Point.objects.count() == 1

    resp = admin_client.get(f'/api/trips/{trip.id}/points/{resp.json()["id"]}')
    assert resp.json()['lat'] == 0.123
    assert resp.json()['lon'] == 1.32
