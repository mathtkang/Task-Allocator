from rest_framework.views import APIView

import time
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_403_FORBIDDEN
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)
from tasks.models import Task, SubTask
from users.models import User
from tasks.serializers import (
    TaskListSerializer, 
    TaskDetailSerializer, 
    SubTaskListSerializer, 
    SubTaskDetailSerializer,
    SubTaskUpdateOnlyCompleteSerializer,
    TaskAutoCompleteSerializer,
)


class Tasks(APIView):
    # 모든 Task 조회
    def get(self, request): 
        '''
        ✅ 모든 사람이 접근 가능
        - subtask의 업무처리 여부에 대해서만 (해당 정보만) 반환 (task_id, subtask_id, complete=F/T) -> filter 참고하기!
        - subtask의 업무 처리 여부(is_complete)확인 가능 : 모든 사람 다 조회 가능 
        - team항목에 user의 team을 넣기 (모델에는 없지만, 조회시 보이도록)
        '''
        all_tasks = Task.objects.all()
        # all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = TaskListSerializer(all_tasks, many=True)
        return Response(serializer.data)

    # task를 생성
    def post(self, request):
        '''
        ✅ 사원만 생성 가능 : 그 사원은 Task > create_user가 됨
        '''
        if request.user.is_authenticated:  # 로그인한 사람만 접근 가능
            serializer = TaskDetailSerializer(data=request.data)
            if serializer.is_valid():
                task = serializer.save(
                    create_user=request.user  # 명시적으로 작성해줌
                )
                serializer = TaskDetailSerializer(task)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
        

class TaskDetail(APIView):
    def get_task_object(self, tid):
        try:
            return Task.objects.get(id=tid)
        except Task.DoesNotExist:
            raise NotFound
    
    def get(self, request, tid):
        task = self.get_task_object(tid)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    # Task 수정
    def put(self, request, tid):
        '''
        ✅ 모든 수정(subtask담당 team 수정 등)은 Task 작성자(create_user)만 가능
        - 모든 subtask가 complete되면 task도 자동으로 complete=True가 된다. -> 이건 subtask의 complete이 변경될 때 신경써줌
        ✅    (즉 task의 complete은 누구도 수정할 수 없다) -> serializer에서 설정 완료!
        - (내가 추가한 부분) 완료된 subtask는 수정 불가능
        '''
        task = self.get_task_object(tid)
        user = request.user
        
        if task.create_user != user:
            return Response(
                {"detail": "해당 task를 수정할 권한이 없음"},
                status=HTTP_403_FORBIDDEN
            )

        serializer = TaskDetailSerializer(
            task,  # 기존에 있던 object
            data=request.data,  # 새롭게 받은 data
            partial=True,  # 부분적 업데이트
        )
        if serializer.is_valid():
            updated_task = serializer.save()

            return Response(
                TaskDetailSerializer(updated_task).data,
            )
        else:
            return Response(serializer.errors)

    # task 삭제
    def delete(self, request, tid):
        '''
        ✅ 완료된 task는 삭제 불가능
        '''
        task = self.get_task_object(tid)
        
        if task.is_complete == True:
            return Response(
                {"detail": "해당 task는 완료되었기 때문에 삭제할 수 없음"},
                status=HTTP_403_FORBIDDEN
            )

        task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class SubTasksAll(APIView):
    # (임시적) 모든 subtask 조회 -> 현재 상태: 모든 사람 다 조회 가능
    def get(self, request):
        all_subtasks = SubTask.objects.all()
        serializer = SubTaskListSerializer(all_subtasks, many=True)
        return Response(serializer.data)


class SubTasks(APIView):
    permission_classes = [IsAuthenticated]

    # validate: task의 아이디가 있는지 확인, task 아이디가 없다면 생성할 수 없음
    def get_task_object(self, tid):
        try:
            return Task.objects.get(id=tid)
        except Task.DoesNotExist:
            raise NotFound

    # (임시적) tid에 해당하는 모든 subtask 조회 -> 현재 상태: 모든 사람 다 조회 가능
    def get(self, request, tid):
        subtasks_of_tid = SubTask.objects.filter(task=tid)  # boolean : + .exists()
        serializer = SubTaskListSerializer(subtasks_of_tid, many=True)
        return Response(serializer.data)
    
    
    # subtask 생성
    def post(self, request, tid): 
        '''
        ✅ 하나의 subtask에는 하나의 team만 설정된다. (팀 설정은 생성자가 설정하는거니까!)
        ✅ 팀 생성시 상위 task 생성자인지 확인 -> task 생성자만 subtask 생성 가능
        '''
        task = self.get_task_object(tid)
        # 지금 타고 온 (url상) task id의 user == user
        if task.create_user == request.user:
            serializer = SubTaskDetailSerializer(data=request.data)
            if serializer.is_valid():
                subtask = serializer.save(
                    task = task
                )
                serializer = SubTaskDetailSerializer(subtask)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            # raise NotAuthenticated
            return Response(
                {"detail": "해당 task의 user가 아니기 때문에 subtask 생성할 수 없음"},
                status=HTTP_403_FORBIDDEN
            )

class SubTaskDetail(APIView):
    def get_task_object(self, tid):
        try:
            return Task.objects.get(id=tid)
        except Task.DoesNotExist:
            raise NotFound
    
    def get_subtask_object(self, tid, stid):
        task = self.get_task_object(tid)
        if task is None:
            raise NotFound
        else:
            try: 
                return SubTask.objects.get(id=stid)
            except SubTask.DoesNotExist:
                raise NotFound
    

    def validate_task_complete(self, tid, data):
        task = self.get_task_object(tid)
        all_subtasks = SubTask.objects.filter(task=tid).all()
        
        subtask_list = []
        for subtask in all_subtasks:
            subtask_list.append(subtask.is_complete)

        auto_serializer = TaskAutoCompleteSerializer(
            task,
            data=data,
        )
        if all(subtask_list) == True:
            if auto_serializer.is_valid():
                auto_serializer.save(
                    is_complete=True,
                )
        elif all(subtask_list) == False:
            if auto_serializer.is_valid():
                auto_serializer.save(
                    is_complete=False,
                )

    # (임시적) subtask 1개 조회
    def get(self, request, tid, stid):
        '''✅ 만약 stid를 만족하는 subtask의 task가 tid와 다르다면 에러발생'''
        subtask = self.get_subtask_object(tid, stid)
        if subtask.task.id != tid:
            raise ValueError  # 요기 에러메시지 쫌 더 생각해보기
        serializer = SubTaskDetailSerializer(subtask)
        return Response(serializer.data)


    # subtask 1개 수정
    def put(self, request, tid, stid):
        '''
        ✅ Task 작성자(create_user)만 : 모든 수정(subtask담당 team 수정 등) 가능
        ✅ 소속 팀원 만 : 완료처리(is_complete) 필드 만 업데이트 가능
        ✅ 모든 subtask.complete=True면 task.complete는 자동으로 True가 된다.
        ✅ subtask.complete가 하나라도 False라면 task.complete는 자동으로 False가 된다.
        '''
        subtask = self.get_subtask_object(tid, stid)
        user = request.user

        # Task 생성자인 경우
        if subtask.task.create_user == user:
            serializer = SubTaskDetailSerializer(
                subtask,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                updated_subtask = serializer.save()

                self.validate_task_complete(tid, request.data)

                return Response(
                    SubTaskDetailSerializer(updated_subtask).data,
                )
            else:
                return Response(serializer.errors)

        # Subtask 소속 팀원인 경우: is_complete 필드 만 업데이트 가능
        elif subtask.team_name == user.team_name:
            serializer = SubTaskUpdateOnlyCompleteSerializer(    # is_complete 만 수정 가능한 시리얼라이저
                subtask,  # 기존에 있던 object
                data=request.data,  # 새롭게 받은 data
                partial=True,  # 부분적 업데이트
            )
            '''
            ✅ 원하는 속성이 아닌 다른 속성이 들어온 경우, 에러 발생! is_complete 속성만 update 해준다.
            '''
            completed_date = request.data.get("completed_date")
            team_name = request.data.get("team_name")

            if completed_date != None or team_name != None:
                return Response(
                    {"detail": "해당 subtask의 completed_date 또는 team_name을 수정할 수 없다. is_complete 만 수정 가능하다."},
                    status=HTTP_400_BAD_REQUEST,
                )
            
            if serializer.is_valid():
                updated_subtask = serializer.save()

                self.validate_task_complete(tid, request.data)

                return Response(
                    SubTaskUpdateOnlyCompleteSerializer(updated_subtask).data,
                )
            else:
                return Response(serializer.errors)
        else:
            # raise NotAuthenticated
            return Response(
                {"detail": "해당 subtask를 할당 받은 팀원이 아니라서 subtask를 수정할 수 없습니다."},
                status=HTTP_403_FORBIDDEN
            )




    # subtask 삭제
    def delete(self, request, tid, stid):
        '''
        ✅ 완료된 subtask는 삭제 불가능
        '''
        subtask = self.get_subtask_object(tid, stid)
        
        if subtask.is_complete == True:
            return Response(
                {"detail": "해당 subtask는 완료되었기 때문에 삭제할 수 없음"},
                status=HTTP_403_FORBIDDEN
            )

        subtask.delete()
        return Response(
            {"detail": f"id가 {stid}인 subtask는 삭제되었습니다."},
            status=HTTP_204_NO_CONTENT
        )