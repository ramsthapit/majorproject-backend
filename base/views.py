from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@api_view(['GET'])
def getLocation(request,pk):
  location = Geolocation.objects.get(id=pk)
  serializer = LocationSerializer(location, many = False)
  return Response(serializer.data)

@api_view(['POST'])
def sendLocation(request):
  data = request.data
  # user = request.user
  location = Geolocation.objects.create(
    # user = user,
    lon = data['lon'], 
    lat = data['lat'], 
  )
  serializer = LocationSerializer(location, many=False)
  return Response(serializer.data)

@api_view(['PUT'])
def updateLocation(request, pk):
  data = request.data
  # user = request.user
  # if(user != data['user']):
  #   content = {'detail': 'Not a valid user'}
  #   return Response(content, status=status.HTTP_400_BAD_REQUEST)
  
  location = Geolocation.objects.get(id=pk)
  serializer = LocationSerializer(location, data=data)
  if serializer.is_valid():
    serializer.save()
  return Response(serializer.data)

@api_view(['DELETE'])
def deleteLocation(request, pk):
  location = Geolocation.objects.get(id=pk)
  location.delete()
  return Response('Location was deleted!')