from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Geolocation
from base.serializers import LocationSerializer
import jwt
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt
import pandas as pd
import numpy as np
from rest_framework import viewsets
from base.models import BusStopLoc, OccupancyCount
from base.serializers import BSLSerializer, CountSerializer
from rest_framework.exceptions import AuthenticationFailed


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
  if not token:
      raise AuthenticationFailed('Unauthenticated!')
  try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated!')

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
  
  token = request.COOKIES.get('jwt')

  if not token:
      raise AuthenticationFailed('Unauthenticated!')
  try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated!')

  if not payload['is_staff']:
      raise AuthenticationFailed('Unauthorized!')

  location = Geolocation.objects.get(id=pk)
  serializer = LocationSerializer(location, data=data)
  if serializer.is_valid():
    serializer.save()
  return Response(serializer.data)


@api_view(['DELETE'])
def deleteLocation(request, pk):
  token = request.COOKIES.get('jwt')

  if not token:
      raise AuthenticationFailed('Unauthenticated!')
  try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated!')

  if not payload['is_staff']:
      raise AuthenticationFailed('Unauthorized!')
  
  location = Geolocation.objects.get(id=pk)
  location.delete()
  return Response('Location was deleted!')


@api_view(['GET'])
def getUserLiveLocation(request,pk):
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
    lat = data['lat'], 
  )
  serializer = LocationSerializer(location, many=False)
  return Response(serializer.data)


@api_view(['POST'])
def recommendBusStop(request):
  userData = request.data
  lon = userData['lon'] 
  lat = userData['lat']
  
  busRoute = BusStopLoc.objects.all()
  serializer = BSLSerializer(busRoute, many=True,context={'request': request})
  loc = []
  busData=[]
  # print(serializer.data[58])
  for i in range(len(serializer.data)):
      # print(i)
      # print(serializer.data[i]['id'])
      la=(lat-serializer.data[i]['lat'])**2
      lo=(lon-serializer.data[i]['lon'])**2

      loc.append([serializer.data[i]['id'], np.sqrt(la+lo)])

  loc.sort(key = lambda row: row[1])
  # print(loc)
  for i in range(len(serializer.data)):
     if serializer.data[i]['id'] == loc[0][0] :
        busData = serializer.data[i]
  
  # print(dataset.iloc[loc[0][0]-1].Address)
  # print(busData)
  location = {
    "id": busData["id"],
    "location": busData["location"],
    "lon": busData['lon'],
    "lat": busData['lat']
  }
  return Response(location)


@api_view(['POST'])
def getBusStop(request):
  data = request.data
  lon = data['lon'] 
  lat = data['lat']
  # print(lon)
  dataset = pd.read_csv('Ringroad.csv')
  # print(lat)
  loc = []
  busData=[]
  for i in range(len(dataset)):
      la=(lat-dataset.iloc[i].Latitude)**2
      lo=(lon-dataset.iloc[i].Longitude)**2

      loc.append([dataset.iloc[i].id, np.sqrt(la+lo)])
      
  loc.sort(key = lambda row: row[1])
  busData = dataset.iloc[loc[0][0]-1]
  location = {
    "id": busData.id,
    "address": busData.Address,
    "lon": busData.Longitude,
    "lat": busData.Latitude
    }
  return Response(location)


@api_view(['GET'])
def getBusStops(request):
  routes = [
    {
      "id": 1,
      "address": "Koteshwor Bus Stop",
      "latitude": 27.6798605245896,
      "longitude": 85.3494035566909
    },
    {
      "id": 2,
      "address": "Balkumari Bus Stop",
      "latitude": 27.6728968589586,
      "longitude": 85.3413558343367
    },
    {
      "id": 3,
      "address": "Khari Ko Bot",
      "latitude": 27.6695162348009,
      "longitude": 85.3363341495496
    },
    {
      "id": 4,
      "address": "Gwarko Bus Stop",
      "latitude": 27.6666041990882,
      "longitude": 85.3319100367766
    },
    {
      "id": 5,
      "address": "B And B",
      "latitude": 27.6661451,
      "longitude": 85.3308219
    },
    {
      "id": 6,
      "address": "Bodhigram Bus Stop",
      "latitude": 27.6609588462165,
      "longitude": 85.3272068137403
    },
    {
      "id": 7,
      "address": "Satdobato Bus Stop",
      "latitude": 27.6590753500787,
      "longitude": 85.3248821671983
    },
    {
      "id": 8,
      "address": "Satdobato Bus Stop",
      "latitude": 27.6586819608226,
      "longitude": 85.3241486835878
    },
    {
      "id": 9,
      "address": "Chakrapath Bus Stop",
      "latitude": 27.6580436040866,
      "longitude": 85.3237470348444
    },
    {
      "id": 10,
      "address": "Talchikhela Choke",
      "latitude": 27.6579240260889,
      "longitude": 85.3225273266858
    },
    {
      "id": 11,
      "address": "JRC Chowk Bus Stop",
      "latitude": 27.6590947959865,
      "longitude": 85.3208635281757
    },
    {
      "id": 12,
      "address": "Mahalaxmisthan Chowk",
      "latitude": 27.6617540800029,
      "longitude": 85.3181909595773
    },
    {
      "id": 13,
      "address": "Thasikhel Chowk",
      "latitude": 27.6638900067431,
      "longitude": 85.3149007509163
    },
    {
      "id": 14,
      "address": "Kusunti Bus Stop",
      "latitude": 27.665365733135,
      "longitude": 85.3124129795437
    },
    {
      "id": 15,
      "address": "Ekantakuna Bus Station",
      "latitude": 27.6671042261907,
      "longitude": 85.3081038710953
    },
    {
      "id": 16,
      "address": "Dhobighat Bus Stop",
      "latitude": 27.6749969429545,
      "longitude": 85.3023297991198
    },
    {
      "id": 17,
      "address": "Sanepa Bus Stop",
      "latitude": 27.6843134970861,
      "longitude": 85.3015217677371
    },
    {
      "id": 18,
      "address": "Balkhu Bus Stop",
      "latitude": 27.6847559353449,
      "longitude": 85.2976424730417
    },
    {
      "id": 19,
      "address": "Kalanki Bus Stop",
      "latitude": 27.6945162195328,
      "longitude": 85.28146253069
    },
    {
      "id": 20,
      "address": "Sitapaila Bus Stop",
      "latitude": 27.7078207893713,
      "longitude": 85.2824709245443
    },
    {
      "id": 21,
      "address": "Swayambhunath Bus Stop",
      "latitude": 27.7160227749464,
      "longitude": 85.2835400303772
    },
    {
      "id": 22,
      "address": "Thulo Bharyang Bus  Stop",
      "latitude": 27.719655554971,
      "longitude": 85.2867550071243
    },
    {
      "id": 23,
      "address": "Sano Bharyang Bus Stop",
      "latitude": 27.7208220782141,
      "longitude": 85.289235751028
    },
    {
      "id": 24,
      "address": "Dhungedhara Bus Stop",
      "latitude": 27.7233824606722,
      "longitude": 85.2946557458332
    },
    {
      "id": 25,
      "address": "Banasthali Chowk",
      "latitude": 27.7249784098851,
      "longitude": 85.297919191683
    },
    {
      "id": 26,
      "address": "Balaju Chowk",
      "latitude": 27.727370707132,
      "longitude": 85.3047845415237
    },
    {
      "id": 27,
      "address": "Machha Pokhari",
      "latitude": 27.7350923432999,
      "longitude": 85.305607916312
    },
    {
      "id": 28,
      "address": "Gongabu Bus Stop",
      "latitude": 27.7350475384409,
      "longitude": 85.3145981398431
    },
    {
      "id": 29,
      "address": "Samakhusi Chowk Bus Stop",
      "latitude": 27.7352039677041,
      "longitude": 85.3183100026393
    },
    {
      "id": 30,
      "address": "Taalim Kendra Bus Stop",
      "latitude": 27.7385260066945,
      "longitude": 85.3257544182211
    },
    {
      "id": 31,
      "address": "Basundhara Chowk Bus Stop",
      "latitude": 27.7422024187004,
      "longitude": 85.3325436481297
    },
    {
      "id": 32,
      "address": "Narayan Gopal Chowk Bus Stop",
      "latitude": 27.7399640384181,
      "longitude": 85.3372380120109
    },
    {
      "id": 33,
      "address": "Chapal Karkhana Bus Stop",
      "latitude": 27.734955356927,
      "longitude": 85.3423343511226
    },
    {
      "id": 34,
      "address": "Dhumbarahi",
      "latitude": 27.7318661633805,
      "longitude": 85.3443264709615
    },
    {
      "id": 35,
      "address": "Sukedhara Bus Stop",
      "latitude": 27.727818398087,
      "longitude": 85.3456822881032
    },
    {
      "id": 36,
      "address": "Gopikrishna",
      "latitude": 27.7216359473363,
      "longitude": 85.3456350201809
    },
    {
      "id": 37,
      "address": "Chabahil",
      "latitude": 27.717644249634,
      "longitude": 85.3465586212818
    },
    {
      "id": 38,
      "address": "Mitrapark",
      "latitude": 27.713123136781,
      "longitude": 85.345497988755
    },
    {
      "id": 39,
      "address": "Jay Bijeshwori",
      "latitude": 27.7103804212202,
      "longitude": 85.3442050613707
    },
    {
      "id": 40,
      "address": "Gaushala",
      "latitude": 27.7074655060081,
      "longitude": 85.3439897378612
    },
    {
      "id": 41,
      "address": "Tilganga Bus Stop",
      "latitude": 27.7062009245992,
      "longitude": 85.3494869813888
    },
    {
      "id": 42,
      "address": "Airport Bus Stop",
      "latitude": 27.700376946417,
      "longitude": 85.3540319393646
    },
    {
      "id": 43,
      "address": "Sinamangal Bus Stop",
      "latitude": 27.694948186201,
      "longitude": 85.3548806910697
    },
    {
      "id": 44,
      "address": "Tinkune Bus Stop",
      "latitude": 27.6875993915326,
      "longitude": 85.3507724251575
    },
    { 
      "id": 45,
      "address": "Koteshwore Bus Stand",
      "latitude": 27.6790049105266,
      "longitude": 85.34972579884
    },
    {
      "id": 46,
      "address": "Soaltee Dobato Chowk",
      "latitude": 27.6765254261313,
      "longitude": 85.3460958782904
    }
  ]
  return Response(routes)


# BusStop CRUDE views
class BSLViewSet(viewsets.ModelViewSet):
    queryset = BusStopLoc.objects.all().order_by('-id')
    serializer_class = BSLSerializer


# factory reset of busStop
@api_view(['get'])
def resetBusRoutes(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    if not payload['is_staff']:
        raise AuthenticationFailed('Unauthorized!')
    
    dataset = pd.read_csv('Ringroad.csv')

    BusStopLoc.objects.all().delete()

    for i in range(len(dataset)):
        # print(dataset.iloc[i].Address)
        busStop = BusStopLoc(
          lat=dataset.iloc[i].Latitude,
          lon = dataset.iloc[i].Longitude,
          location= dataset.iloc[i].Address
        )
        busStop.save()
    return Response("Bus Stop are Added")


class OCViewSet(viewsets.ModelViewSet):
    queryset = OccupancyCount.objects.all().order_by('-id')
    serializer_class = CountSerializer

@api_view(['GET'])
def getLiveOccupancyCount(request,pk):
  count = OccupancyCount.objects.filter(bus_id=pk).order_by('-id')[0:1]
  serializer = CountSerializer(count, many=True, context={'request': request})
  return Response(serializer.data)