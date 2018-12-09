from django.contrib.auth.models import User
from django.db import models


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Point(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,
                             related_name='points')

    time = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lon = models.FloatField()
    elevation = models.FloatField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    speed = models.FloatField(default=0, blank=True, null=True)
    satellites = models.IntegerField(blank=True, null=True)
    provider = models.CharField(blank=True, null=True, max_length=100)
    activity = models.CharField(blank=True, null=True, max_length=100)
    battery = models.FloatField(blank=True, null=True)
    annotation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'<Point {self.lat} {self.lon}>'
