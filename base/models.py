from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  username = None

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return str(self.email)

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