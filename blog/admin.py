from django.contrib import admin
from .models import BlogPost, Tag


admin.site.register(Tag)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "created", "updated"]
    list_filter = ["created", "updated", "published", "tags"]
    search_fields = ["title", "body_md"]

