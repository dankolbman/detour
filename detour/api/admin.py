from django.contrib import admin
from .models import Trip, Point, Post


admin.site.register(Point)
admin.site.register(Post)


class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'visible', 'order', 'owner', 'name', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('visible', 'order')


admin.site.register(Trip, TripAdmin)
