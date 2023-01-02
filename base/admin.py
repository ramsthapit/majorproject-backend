from django.contrib import admin

# Register your models here.

from .models import Geolocation, User
admin.site.register(Geolocation)
admin.site.register(User)