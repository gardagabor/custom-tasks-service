from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    # ex: /tasks/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:task_id>/", views.detail, name="detail"),
    # ex: /tasks/5/
    path("<int:task_id>/", views.create_task, name="create_task"),
]