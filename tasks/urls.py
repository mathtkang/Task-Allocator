from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

app_name = "users"

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("<int:id>", views.SelectUser.as_view()),
]

