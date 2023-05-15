from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

urlpatterns = [
    # end-point
    path('admin/', admin.site.urls),
    path("v1/tasks/", include("tasks.urls")),
    path("v1/users/", include("users.urls")),
]
