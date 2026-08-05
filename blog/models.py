from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator

from core.utils import render_markdown


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag_detail", args=[self.slug])


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    excerpt = models.CharField(max_length=300, blank=True)
    body_md = models.TextField()

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts"
    )
    discussion_url = models.URLField(blank=True)

    published = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    
    @property
    def summary(self):
        if self.excerpt:
            return self.excerpt
        html = render_markdown(self.body_md)
        text = strip_tags(html)
        return Truncator(text).words(30)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post", args=[self.slug])

