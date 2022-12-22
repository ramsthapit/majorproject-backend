from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Geolocation(models.Model):
  # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  lon = models.FloatField(null=True)
  lat = models.FloatField(null=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.lon)

  class Meta:
    ordering = ['-updated']