from django.contrib import admin

# Register your models here.

from .models import Geolocation
admin.site.register(Geolocation)