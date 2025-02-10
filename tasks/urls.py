from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    # ex: /tasks/
    path("", views.index, name="index"),
    # ex: /tasks/5/
    path("<int:task_id>/", views.handle_task, name="handle_task"),
]