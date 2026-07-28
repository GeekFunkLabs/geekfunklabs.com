from django.shortcuts import render
from django.views.generic import DetailView

from .models import Project

def projects(request):
    return render(
        request,
        "projects/project_list.html",
        {
            "active": Project.objects.filter(status="active"),
            "experimental": Project.objects.filter(status="experimental"),
            "archived": Project.objects.filter(status="archived"),
        }
    )            

class ProjectView(DetailView):
    model = Project

