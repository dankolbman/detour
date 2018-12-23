import pytest
import base64
from django.contrib.auth.models import User


@pytest.mark.parametrize('url,method', [
    ('/api/trips', 'POST'),
    ('/api/trips/{trip_id}', 'PATCH'),
    ('/api/trips/{trip_id}/points', 'POST'),
    ('/api/trips/{trip_id}/points/{point_id}', 'PATCH'),
])
def test_not_authorized(client, db, point, url, method):
    r = getattr(client, method.lower())
    resp = r(url.format(trip_id=point.trip_id, point_id=point.id))
    assert resp.status_code in [401, 403]


@pytest.mark.parametrize('url,method', [
    ('/api/trips', 'GET'),
    ('/api/trips/{trip_id}', 'PATCH'),
    ('/api/trips/{trip_id}/points', 'GET'),
    ('/api/trips/{trip_id}/points/{point_id}', 'PATCH'),
])
def test_is_authorized(client, db, point, url, method):
    auth = f"Basic {base64.b64encode(b'testy:pass').decode('ascii')}"
    r = getattr(client, method.lower())
    resp = r(url.format(trip_id=point.trip_id, point_id=point.id),
             HTTP_AUTHORIZATION=auth)

    assert resp.status_code == 200


def test_not_owner_new_point(client, db, trip):
    """ Try to add a point to a trip with a different owner """
    user = User.objects.create(username='test')
    user.set_password('abc')
    user.save()

    auth = f"Basic {base64.b64encode(b'test:abc').decode('ascii')}"
    assert user.id != trip.owner.id
    resp = client.post(f'/api/trips/{trip.id}/points',
                       data={
                           'lat': 1.11,
                           'lon': 2.22,
                           'trip': trip.id,
                           'time': f'2019-01-01T00:00',
                       },
                       HTTP_AUTHORIZATION=auth)
    assert resp.status_code == 403
