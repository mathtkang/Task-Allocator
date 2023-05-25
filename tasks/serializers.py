from rest_framework.serializers import ModelSerializer
from tasks.models import Task, SubTask
from users.serializers import SignUpSerializer, PublicUserSerializer


class TaskListSerializer(ModelSerializer):
    create_user = SignUpSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskDetailSerializer(ModelSerializer):
    create_user = SignUpSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "is_complete",
        )


class SubTaskListSerializer(ModelSerializer):
    create_user = PublicUserSerializer(read_only=True)

    class Meta:
        model = SubTask
        fields = "__all__"


class TinyTaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "is_complete",
            "create_user",
        )


class SubTaskDetailSerializer(ModelSerializer):
    task = TinyTaskSerializer(read_only=True)
    
    class Meta:
        model = SubTask
        fields = "__all__"


class SubTaskSerializer(ModelSerializer):
    
    class Meta:
        model = SubTask
        fields = (
            "id",
            "is_complete",
            "completed_date",
            "team_name",
        )

class TaskandSubtaskListSerializer(ModelSerializer):
    create_user = PublicUserSerializer(read_only=True)
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "create_user",
            "title",
            "content",
            "is_complete",
            "subtasks",
            "created_at",
            "updated_at",
        )


class SubTaskUpdateOnlyCompleteSerializer(ModelSerializer):

    class Meta:
        model = SubTask
        fields = (
            "is_complete",
        )


class TaskAutoCompleteSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "is_complete",
        )