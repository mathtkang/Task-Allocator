import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

from users import models as m
from users.serializers import SignUpSerializer, MeSerializer


# DONE
class SignUp(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 모델 객체가 만들어지고, 모델 객체의 값들이 할당이 다 된 model.save()가 호출이 되는 것이다.
            # user.password = password  # We Don't Do this!
            user.set_password(password)  # set_password() is hashed pw method of django
            user.save()  # 이때 db에 user object가 저장됨
            serializer = SignUpSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# DONE
class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response(
                {"ok": "Welcome!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "wrong password"})


# DONE
class LogOut(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 상태

    def post(self, request):
        logout(request)
        return Response(
            {"ok": "bye!"}, 
            status=status.HTTP_200_OK
        )


# DONE
class Me(APIView):  # team_name은 로그인 한 다음에 바꿀 수 있다.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MeSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = MeSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = MeSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                # serializer.errors
                {"detail": "Please request one of the 7 team names"}, 
                status=status.HTTP_400_BAD_REQUEST,
            )


# TODO
class Todo(APIView):  # 업무목록 조회
    # - subtask의 팀원이라면(권한) → 업무목록에서 함께 조회가 가능해야 함
    pass