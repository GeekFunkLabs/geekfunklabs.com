from django.db.models import Case, IntegerField, When
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Project


class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        return (
            Project.objects.annotate(
                status_order=Case(
                    When(status="active", then=0),
                    When(status="experimental", then=1),
                    When(status="archived", then=2),
                    output_field=IntegerField(),
                )
            )
            .order_by("status_order", "name")
        )

class ProjectView(DetailView):
    model = Project

