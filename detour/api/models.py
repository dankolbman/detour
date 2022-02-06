from datetime import datetime
from haversine import haversine

from django.contrib.auth.models import User
from django.db import models


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=100,
        default="name",
        help_text="Used for identification of the trip",
    )
    name = models.CharField(max_length=100, help_text="A short title for the trip")
    description = models.TextField(help_text="A short blurb about the trip")
    visible = models.BooleanField(
        default=False,
        help_text="Whether to show the trip on the site or not",
    )
    order = models.PositiveIntegerField(default=100)
    icon = models.ImageField(upload_to="uploads/", max_length=100, blank=True)

    location = models.CharField(
        max_length=1024,
        default="The world",
        help_text="Where the trip occurred geographically",
    )
    trip_time = models.CharField(
        help_text="A textual description of when the trip occurred such as 'spring 2029'",
        max_length=256,
        blank=True,
    )
    trip_start = models.DateTimeField(
        help_text="When the trip started",
        null=False,
        default=datetime.utcnow,
    )
    trip_end = models.DateTimeField(
        help_text="When the trip ended",
        null=False,
        default=datetime.utcnow,
    )

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
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="posts")

    author = models.CharField(max_length=512, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()


class Memory(models.Model):
    """
    A memory is a quick note or picture and caption of something that happened
    on a trip.
    """

    class Meta:
        verbose_name_plural = "memories"

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="memories",
        help_text="The associated trip",
    )

    title = models.TextField(
        help_text="The name of this memory",
    )
    description = models.TextField(
        blank=True,
        help_text="A short blurb about the trip",
    )
    image = models.ImageField(
        upload_to="uploads/",
        max_length=1024,
        blank=True,
        help_text="An associated image",
    )
    time = models.DateTimeField(
        blank=False,
        help_text="When this memory occurred",
    )
    location = models.CharField(
        blank=True,
        max_length=1024,
        help_text="Where this memory happened",
    )
    lat = models.FloatField(
        blank=True,
        null=True,
        help_text="latitude if available",
    )
    lon = models.FloatField(
        blank=True,
        null=True,
        help_text="longitude if available",
    )

    def __str__(self):
        return f"{self.title}"
