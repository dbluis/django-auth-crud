from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.signin, name="singin"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/complete",
         views.task_completed, name="task_completed"),
    path("tasks/<int:task_id>/delete",
         views.task_delete, name="task_delete"),
    path("finish_tasks", views.finish_tasks, name="finish_tasks"),
]
