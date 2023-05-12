import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

from users import models as m
from users import serializers as s


class SignUP(APIView):
    pass


class Me(APIView):
    pass


class SelectUser(APIView):
    pass
