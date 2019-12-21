import factory
import pytz
import random

from django.contrib.auth.models import User

from .models import Trip, Point


class TripFactory(factory.DjangoModelFactory):
    class Meta:
        model = Trip

    owner = factory.Iterator(User.objects.all())
    name = factory.Faker("bs")
    description = factory.Faker("bs")


class PointFactory(factory.DjangoModelFactory):
    class Meta:
        model = Point

    trip = factory.Iterator(Trip.objects.all())

    lat = factory.Sequence(lambda n: random.random() * 180 - 90)
    lon = factory.Sequence(lambda n: random.random() * 360 - 180)
    time = factory.Faker(
        "date_time_between", start_date="-2y", end_date="now", tzinfo=pytz.UTC
    )
