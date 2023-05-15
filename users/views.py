import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import query

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from users.models import User
from users.serializers import SignUpSerializer, MeSerializer
from tasks.models import Task, SubTask
from tasks.serializers import SubTaskDetailSerializer, TaskandSubtaskListSerializer


class SignUp(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = SignUpSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


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
                {"detail": "로그인 되었습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "비밀번호가 틀렸습니다."},
                status=HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"ok": "bye!"}, 
            status=HTTP_200_OK,
        )


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
                {"detail": "지정된 7개의 팀명 중 하나의 팀명으로 입력해주세요."}, 
                status=status.HTTP_400_BAD_REQUEST,
            )


class Todo(APIView):  # 업무목록 조회
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        ✅ 하위업무(SubTask)에 본인 팀이 포함되어 있다면, 업무목록에서 업무(Task)도 함께 조회 가능
        = subtask의 팀원이면(권한) → 업무목록(해당 라우터)에서 상위 Task에 따른 모든 Subtask도 함께 조회 가능 
            (그래야 본인팀의 subtask 완료와 함께 task를 완료하기 위해서는 추가적으로 어떤 subtask의 완료가 필요한지 알 수 있기 때문)
        '''
        user = request.user
        all_subtasks = SubTask.objects.filter(team_name=user.team_name).all()  
        
        tasks_list = []
        for subtask in all_subtasks:
            tasks = Task.objects.get(id=subtask.task.id)
            if tasks not in tasks_list:
                tasks_list.append(tasks)

        serializer = TaskandSubtaskListSerializer(tasks_list, many=True)
        return Response(serializer.data)

        '''
        (경우2) subtast의 팀원인 경우, subtask_list만 보고 싶다면 아래 코드로 동작
        '''
        # user = request.user
        # all_subtasks = SubTask.objects.filter(team_name=user.team_name).all()  
        # serializer = SubTaskDetailSerializer(all_subtasks, many=True)
        # return Response(serializer.data)