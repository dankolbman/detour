from haversine import haversine

from django.contrib.auth.models import User
from django.db import models


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    visible = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=100)
    icon = models.ImageField(upload_to="uploads/", max_length=100, blank=True)

    def __str__(self):
        return f"{self.name}"

    def distance(self, resolution=100):
        """ Return cumulative distance as a function of time """
        points = (
            self.points.values("lat", "lon", "time").all().order_by("time")
        )

        def dist(p1, p2):
            return haversine((p1["lat"], p1["lon"]), (p2["lat"], p2["lon"]))

        distances = []
        dr = 0
        for i in range(len(points) - 1):
            d = dist(points[i + 1], points[i])
            # if d > 0.5:
            #     continue
            dr += d
            if i % resolution != 0:
                continue
            distances.append({"time": points[i]["time"], "distance": dr})

        return distances


class Point(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="points"
    )

    time = models.DateTimeField()
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
        return f"<Point {self.lat} {self.lon}>"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="posts"
    )

    author = models.CharField(max_length=512, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
