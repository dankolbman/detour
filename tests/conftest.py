import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from detour.api.models import Point, Trip


BASE_URL = 'http://testserver'


@pytest.fixture
def user(db):
    user = User.objects.create(username='testy')
    user.set_password('pass')
    user.save()
    return user


@pytest.fixture
def trip(user):
    trip = Trip.objects.create(name='Test trip', owner_id=user.id)
    return trip


@pytest.fixture
def point(trip):
    point = Point.objects.create(time='2019-01-01T00:00Z',
                                 trip_id=trip.id,
                                 lat=1.11,
                                 lon=1.22)
    return point
