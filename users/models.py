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
    class TeamChoices(models.TextChoices):
        SOPHIA = ("sophia", "Sophia")
        ISABELLA = ("isabella", "Isabella")
        LINA = ("lina", "Lina")
        NOAH = ("noah", "Noah")

    username = models.CharField(
        max_length=128,
        unique=True,
    )
    team_name = models.CharField(
        max_length=50,
        choices=TeamChoices.choices,
    )