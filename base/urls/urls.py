from django.urls import path
from base.views import views

urlpatterns = [
    path('', views.getRoutes),
]
