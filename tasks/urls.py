from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    # ex: /tasks/
    path("", views.index, name="index"),
    # ex: /tasks/
    path("create/", views.create_task, name="create_task"),
]