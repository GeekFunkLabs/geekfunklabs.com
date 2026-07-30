from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("<slug:slug>", views.ProjectView.as_view(), name="project"),
]

