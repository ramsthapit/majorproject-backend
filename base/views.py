from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Geolocation
from .serializers import LocationSerializer

@api_view(['GET'])
def getRoutes(request):
  return Response("hello there !")

@api_view(['GET'])
def getLocations(request):
  locations = Geolocation.objects.all()
  serializer = LocationSerializer(locations, many = True)
  return Response(serializer.data)