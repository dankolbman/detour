from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Point, Trip


class TripSerializer(serializers.HyperlinkedModelSerializer):
    points = serializers.HyperlinkedIdentityField(
        view_name='trip-points-list',
        lookup_url_kwarg='trip_pk'
    )
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Trip
        fields = ('id', 'created_at', 'name', 'owner', 'description', 'points')



class PointSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Point
        fields = ('id', 'time', 'lat', 'lon', 'elevation', 'accuracy',
                  'satellites', 'provider', 'activity', 'battery',
                  'annotation', 'trip')

        validators = [
                    UniqueTogetherValidator(
                        queryset=Point.objects.all(),
                        fields=('time', 'lat', 'lon'),
                        message='point already exists'
                    )
                ]
