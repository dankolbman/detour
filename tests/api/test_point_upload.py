import pytest
import datetime
import random
from detour.api.models import Point, Trip


def points(n):
    header = ','.join(['time,lat,lon,elevation,accuracy,bearing,speed',
                       'satellites,provider,hdop,vdop,pdop,geoidheight',
                       'ageofdgpsdata,dgpsid,activity,battery,annotation'])
    point = "{},{},{},-8.0,7.585,,0.0,0,gps,,,,,,,UNKNOWN,62,\n"
    body = []
    for _ in range(n):
        body.append(point.format(datetime.datetime.now().isoformat(),
                    random.randrange(-90, 90),
                    random.randrange(-180, 180)))

    return header + '\n' + ''.join(body)


def test_upload_csv(client, user, trip, db):
    data = points(100)
    resp = client.put(f'/remote.php/webdav/{trip.id}/20181205180216.csv',
                      content_type='text/octet-stream',
                      data=data)

    assert resp.status_code == 201
    assert Point.objects.count() == 100
