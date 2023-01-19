from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Geolocation
from base.serializers import LocationSerializer
import jwt
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt
import pandas as pd
import numpy as np

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

@csrf_protect
@requires_csrf_token
@api_view(['POST'])
def sendLocation(request):
  data = request.data
  token = request.COOKIES.get('jwt')
  payload = jwt.decode(token, 'secret', algorithms=['HS256'])

  user = payload['id']
  location = Geolocation.objects.create(
    user = user,
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

@api_view(['GET'])
def getUserLocation(request,pk):
  location = Geolocation.objects.filter(user=pk).order_by('-id')[0:1]
  serializer = LocationSerializer(location, many=True)
  return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def sendLocationUser(request,pk):
  data = request.data
  # token = request.COOKIES.get('jwt')
  # payload = jwt.decode(token, 'secret', algorithms=['HS256'])

  # user = payload['id']
  location = Geolocation.objects.create(
    user = pk,
    lon = data['lon'], 
    lat = request.data['lat'], 
  )
  serializer = LocationSerializer(location, many=False)
  return Response(serializer.data)

@api_view(['POST'])
def getBusStop(request):
  data = request.data
  lon = data['lon'] 
  lat = request.data['lat']
  dataset = pd.read_csv('Ringroad.csv')

  loc = []

  for i in range(len(dataset)):
      la=(lat-dataset.iloc[i].Latitude)**2
      lo=(lon-dataset.iloc[i].Longitude)**2

      loc.append([dataset.iloc[i].id, np.sqrt(la+lo)])

  min=loc[i][1]
  id = 0
  for i in range(len(loc)):
    if min > loc[i][1]:
        min = loc[i][1]
        id = loc[i][0]
  busData = dataset.iloc[loc[id-1][0]]

  location = {
    "id": busData.id,
    "address": busData.Address,
    "lon": busData.Longitude,
    "lat": busData.Latitude
  }
  return Response(location)