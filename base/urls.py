from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('location/', views.getLocations),
    path('location/create', views.sendLocation),
    path('location/<str:pk>/update/', views.updateLocation),
    path('location/<str:pk>/delete/', views.deleteLocation),
    path('location/<str:pk>', views.getLocation),
    path("users/register/", views.RegisterView.as_view()),
    path("users/login/", views.LoginView.as_view()),
]
