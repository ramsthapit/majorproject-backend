from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('', views.UsersView.as_view(), name="getUsers"),
    path("register/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("profile/", views.UserView.as_view()),
    path("update/", views.UpdateProfileView.as_view()),
    path("update/<str:pk>/", views.UpdateUserView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("delete/<str:pk>/", views.DeleteUserView.as_view()),
]
