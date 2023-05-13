from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.Tasks.as_view()),
    path("<int:tid>", views.TaskDetail.as_view()),
    path("<int:tid>/subtasks", views.SubTasks.as_view()),
    path("<int:tid>/subtasks/<int:stid>", views.SubTaskDetail.as_view()),
]