from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Point, Trip


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
