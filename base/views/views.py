from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
  routes = [
    {
      'Endpoint': '/location/',
      'method': 'GET',
      'body': None,
      'description': 'Returns an array of locations'
    },
    {
      'Endpoint': '/location/id',
      'method': 'GET',
      'body': None,
      'description': 'Returns a single location object'
    },
    {
      'Endpoint': '/location/create',
      'method': 'POST',           
      'description': 'Creates a new location with data sent in post request'
    },
    {
      'Endpoint': '/location/id/update',
      'method': 'PUT',
      'description': 'Updates an existing location with data sent in the request'
    },
    {
      'Endpoint': '/location/id/delete',
      'method': 'DELETE',
      'description': 'Deletes an existing location'
    },
  ]
  return Response(routes)
