from django.shortcuts import render

from blog.models import BlogPost
from projects.models import Project


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "featured_projects": Project.objects.filter(
                status="active"
            ).order_by("name")[:3],
            "recent_posts": BlogPost.objects.filter(
                published=True
            ).order_by("-created")[:3],
        },
    )

def about(request):
    return render(request, "core/about.html")
