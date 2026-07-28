from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path("", views.projects, name="index"),
    path("<slug:slug>/", views.ProjectView.as_view(), name="detail"),
]

