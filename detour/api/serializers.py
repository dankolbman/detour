from rest_framework import serializers
from .models import Point, Trip


class PointSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Point
        fields = ('id', 'time', 'lat', 'lon', 'elevation', 'accuracy',
                  'satellites', 'provider', 'activity', 'battery',
                  'annotation', 'trip')
