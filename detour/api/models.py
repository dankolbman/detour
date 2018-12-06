from django.db import models


class Point(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    time = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lon = models.FloatField()
    elevation = models.FloatField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    satellites = models.IntegerField(blank=True, null=True)
    provider = models.CharField(blank=True, null=True, max_length=100)
    activity = models.CharField(blank=True, null=True, max_length=100)
    battery = models.FloatField(blank=True, null=True)
    annotation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'<Point {self.lat} {self.lon}>'
