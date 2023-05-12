from django.db import models
from common.models import CommonModel


class Task(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    create_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    # task의 team 속성은 없앴다.


class SubTask(models.Model):
    class TeamChoices(models.TextChoices):
        DANBI = ("danbi", "Danbi")   # 단비
        DARAE = ("darae", "Darae")   # 다래
        BLABLA = ("blabla", "Blabla") # 블라블라
        CHEOLLO = ("cheollo", "Cheollo") # 철로
        TANGII = ("tangii", "Tangii") # 땅이
        HAETAE = ("haetae", "Haetae")  # 해태
        SUPI = ("supi", "Supi")  # 수피
    
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(
        "tasks.Task",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="subtasks",
    )
    team_name = models.CharField(
        max_length=50,
        choices=TeamChoices.choices,
    )
    # team = models.ForeignKey(
    #     "tasks.Team",
    #     on_delete=models.CASCADE,
    #     related_name="subtasks",
    # )


class Team(models.Model):
    class TeamChoices(models.TextChoices):
        DANBI = ("danbi", "Danbi")   # 단비
        DARAE = ("darae", "Darae")   # 다래
        BLABLA = ("blabla", "Blabla") # 블라블라
        CHEOLLO = ("cheollo", "Cheollo") # 철로
        TANGII = ("tangii", "Tangii") # 땅이
        HAETAE = ("haetae", "Haetae")  # 해태
        SUPI = ("supi", "Supi")  # 수피
    
    name = models.CharField(
        max_length=50,
        choices=TeamChoices.choices,
    )
    member = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="teams",
    )