from django.urls import path
from base.views import location_views as views

urlpatterns = [
    path('', views.getLocations),
    path('create/', views.sendLocation),
    path('<str:pk>/update/', views.updateLocation),
    path('<str:pk>/delete/', views.deleteLocation),
    path('<str:pk>/', views.getLocation),
]
