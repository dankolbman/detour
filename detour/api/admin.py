from django.contrib import admin
from .models import Trip, Point, Post


class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "visible", "order", "owner", "name", "created_at")
    list_display_links = ("id", "name")
    list_editable = ("visible", "order")


admin.site.register(Trip, TripAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "trip")
    list_display_links = ("id", "author")


admin.site.register(Post, PostAdmin)


class PointAdmin(admin.ModelAdmin):
    list_display = ("id", "trip", "created_at", "lat", "lon")
    list_display_links = ("id",)
    list_filter = ("trip", "time")


admin.site.register(Point, PointAdmin)
