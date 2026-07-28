from django.db import models
from django.urls import reverse
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    summary = models.CharField(max_length=300)

    description_md = models.TextField()

    docs_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    store_url = models.URLField(blank=True)
    discussion_url = models.URLField(blank=True)

    cover_image = models.ImageField(
        upload_to="project_images/featured/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("experimental", "Experimental"),
            ("archived", "Archived"),
        ],
        default="active"
    )

    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(upload_to="project_images/gallery/")

    caption = models.CharField(max_length=200, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.name} image"

