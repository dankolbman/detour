from rest_framework import serializers
from .models import Point


class PointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Point
        fields = ('id', 'time', 'lat', 'lon', 'elevation', 'accuracy', 'speed',
                  'satellites', 'provider', 'activity', 'battery',
                  'annotation')
