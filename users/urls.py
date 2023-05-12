from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

app_name = "users"

urlpatterns = [
    path("signup", views.SignUp.as_view()),
    path("login", views.LogIn.as_view()),
    path("logout", views.LogOut.as_view()),
    path("me", views.Me.as_view()),
]

