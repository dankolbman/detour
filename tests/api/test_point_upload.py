import pytest
import datetime
import random
from detour.api.models import Point, Trip
from detour.api.serializers import PointSerializer


def header():
    return ','.join(['time,lat,lon,elevation,accuracy,bearing,speed',
                     'satellites,provider,hdop,vdop,pdop,geoidheight',
                     'ageofdgpsdata,dgpsid,activity,battery,annotation'])
def points(n):
    point = "{},{},{},-8.0,7.585,,0.0,0,gps,,,,,,,UNKNOWN,62,\n"
    body = []
    for _ in range(n):
        body.append(point.format(datetime.datetime.now().isoformat(),
                    random.randrange(-90, 90),
                    random.randrange(-180, 180)))

    return header() + '\n' + ''.join(body)


def test_upload_csv(admin_client, user, trip, db):
    data = points(100)
    resp = admin_client.put(f'/remote.php/webdav/{trip.id}/20181205180216.csv',
                      content_type='text/octet-stream',
                      data=data)

    assert resp.status_code == 201
    assert Point.objects.count() == 100


def test_upload_invalid(admin_client, user, trip, db):
    data = points(100)
    # Add invalid point
    l = data.split('\n')[2].split(',')
    l[1] = 'blah'
    l = ','.join(l)
    data += l

    resp = admin_client.put(f'/remote.php/webdav/{trip.id}/20181205180216.csv',
                      content_type='text/octet-stream',
                      data=data)

    assert resp.status_code == 201
    assert Point.objects.count() == 100
    assert resp.json()['errors'] == [{'lat': ['A valid number is required.']}]
    assert resp.json()['message'] == 'Added 100 points'


def test_no_dupes(admin_client, user, trip, db):
    """ Test that points are not created more than once """
    data = points(10)
    resp = admin_client.put(f'/remote.php/webdav/{trip.id}/20181205180216.csv',
                      content_type='text/octet-stream',
                      data=data)
    assert resp.status_code == 201
    assert Point.objects.count() == 10

    resp = admin_client.put(f'/remote.php/webdav/{trip.id}/20181205180216.csv',
                      content_type='text/octet-stream',
                      data=data)
    assert resp.status_code == 201
    assert Point.objects.count() == 10
