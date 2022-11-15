from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Geolocation(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  lon = models.DecimalField(max_digits=8, decimal_places=3, null=True,)
  lat = models.DecimalField(max_digits=8, decimal_places=3, null=True,)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.user)

  class Meta:
    ordering = ['-updated']