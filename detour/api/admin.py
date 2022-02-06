from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Trip, Memory, Point, Post


class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "visible", "order", "owner", "name", "created_at")
    list_display_links = ("id", "name")
    list_editable = ("visible", "order")


admin.site.register(Trip, TripAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "trip")
    list_display_links = ("id", "author")


admin.site.register(Post, PostAdmin)


class PointAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "trip", "created_at", "lat", "lon")
    list_display_links = ("id",)
    list_filter = ("trip", "time")


admin.site.register(Point, PointAdmin)


class MemoryAdmin(admin.ModelAdmin):
    list_display = ("title", "trip", "location", "owner", "time")
    list_display_links = ("title",)
    list_filter = ("trip", "owner")


admin.site.register(Memory, MemoryAdmin)
