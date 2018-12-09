import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from detour.api.models import Point, Trip


BASE_URL = 'http://testserver'


@pytest.fixture
def user(db):
    user = User.objects.create(username='testy')
    return user


@pytest.fixture
def trip(user):
    trip = Trip.objects.create(name='Test trip', owner_id=user.id)
    return trip
