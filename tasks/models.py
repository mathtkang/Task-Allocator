from django.db import models


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


class SubTask(models.Model):
    class TeamChoices(models.TextChoices):
        SOPHIA = ("sophia", "Sophia")
        ISABELLA = ("isabella", "Isabella")
        LINA = ("lina", "Lina")
        NOAH = ("noah", "Noah")
    
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    team_name = models.CharField(
        max_length=50,
        choices=TeamChoices.choices,
    )