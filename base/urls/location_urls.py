from django.urls import path, include
from base.views import location_views as views
from rest_framework import routers

router = routers.DefaultRouter()
router1 = routers.DefaultRouter()
router.register(r'', views.BSLViewSet)
router1.register(r'',views.OCViewSet)

urlpatterns = [
    path('', views.getLocations),
    path('create/', views.sendLocation),
    path('create/<str:pk>/', views.sendLocationUser),
    path('busroutes/',include(router.urls)),
    path('buscount/',include(router1.urls)),
    path('resetbusroutes/', views.resetBusRoutes),
    path('recommend/', views.getBusStop),
    path('busstop/', views.recommendBusStop),
    path('busstops/', views.getBusStops),
    path('<str:pk>/update/', views.updateLocation),
    path('<str:pk>/delete/', views.deleteLocation),
    path('<str:pk>/', views.getLocation),
    path('<str:pk>/live/', views.getUserLiveLocation),
    path('<str:pk>/live/occupancycount/', views.getLiveOccupancyCount),
]
