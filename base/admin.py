from django.contrib import admin

# Register your models here.

from .models import geolocation
admin.site.register(geolocation)