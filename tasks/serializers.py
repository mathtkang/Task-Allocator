from rest_framework.serializers import ModelSerializer
from tasks.models import Task, SubTask
from users.serializers import SignUpSerializer


class TaskListSerializer(ModelSerializer):
    create_user = SignUpSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskDetailSerializer(ModelSerializer):
    # custom serializer
    create_user = SignUpSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "is_complete",
        )


class SubTaskListSerializer(ModelSerializer):
    create_user = SignUpSerializer(read_only=True)

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
    # custom serializer
    task = TinyTaskSerializer(read_only=True)
    
    class Meta:
        model = SubTask
        fields = "__all__"


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