from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Point, Trip


class TripSerializer(serializers.HyperlinkedModelSerializer):
    points = serializers.HyperlinkedIdentityField(
        view_name='trip-points-list',
        lookup_url_kwarg='trip_pk'
    )
    linestring = serializers.HyperlinkedIdentityField(
        view_name='trip-linestring',
        lookup_url_kwarg='pk'
    )
    speed = serializers.HyperlinkedIdentityField(
        view_name='trip-speed',
        lookup_url_kwarg='pk'
    )
    annotations = serializers.HyperlinkedIdentityField(
        view_name='trip-annotations',
        lookup_url_kwarg='pk'
    )
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Trip
        fields = ('id', 'created_at', 'name', 'owner', 'description', 'points',
                  'linestring', 'speed', 'annotations')



class PointSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Point
        fields = ('id', 'time', 'lat', 'lon', 'elevation', 'accuracy',
                  'speed', 'satellites', 'provider', 'activity', 'battery',
                  'annotation', 'trip')

        validators = [
                    UniqueTogetherValidator(
                        queryset=Point.objects.all(),
                        fields=('time', 'lat', 'lon'),
                        message='point already exists'
                    )
                ]
