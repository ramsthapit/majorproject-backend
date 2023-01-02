from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('', views.getUsers, name="getUsers"),
    path("register/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("profile/", views.UserView.as_view()),
    path("logout/", views.LogoutView.as_view()),
]
