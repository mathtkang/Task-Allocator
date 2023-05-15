from rest_framework.serializers import ModelSerializer
from users.models import User


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            # password를 입력하면 hashed된 pw가 db에 저장된다.
        )


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "team_name",
        )


class MeSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "id",
            "email",
            "password",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )