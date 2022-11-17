from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('location/', views.getLocations),
    path('location/create', views.sendLocation),
    path('location/<str:pk>/update/', views.updateLocation),
    path('location/<str:pk>/delete/', views.deleteLocation),
    path('location/<str:pk>', views.getLocation),
]
