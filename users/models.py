from django.db import models
from django.contrib.auth.models import AbstractUser

"""
[AbstractUser에서 기본적으로 제공하는 필드]
* id (pk, not null, int)
* username (not null, char)
* email (char-emailField)
* password (not null)
* last_login (not null, dateTime)
* date_joined (not null, dateTime)
"""

class User(AbstractUser):
    # id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=128,
        unique=True,
    )
    # team_name = models.CharField(max_length=128)
    team = models.ForeignKey(
        "tasks.Team",
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="users",
    )