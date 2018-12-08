from django.contrib import admin
from .models import Trip, Point


admin.site.register(Point)

class TripAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'created_at')

admin.site.register(Trip, TripAdmin)
