from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Geolocation
from base.serializers import LocationSerializer
import jwt
from django.views.decorators.csrf import csrf_protect, requires_csrf_token

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