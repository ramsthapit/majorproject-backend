from django.http import JsonResponse

def getRoutes(request):
  return JsonResponse("hello there !", safe=False)
