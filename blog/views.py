from django.db.models import Count, Q   
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import BlogPost, Tag
from core.utils import github_create_discussion


def post_source(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return HttpResponse(
        post.body_md,
        content_type="text/markdown; charset=utf-8",
    )


def discuss(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if not post.discussion_url:
        post.discussion_url = github_create_discussion(post)
        post.save(update_fields=["discussion_url"])
    return redirect(post.discussion_url)


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(published=True)
            .prefetch_related("tags")
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = (
            Tag.objects
            .annotate(
                num_posts=Count(
                    "posts",
                    filter=Q(posts__published=True)
                )
            )
            .filter(num_posts__gt=0)
            .order_by("-num_posts")
        )
        context["archive"] = (
            BlogPost.objects
                .filter(published=True)
                .annotate(year=ExtractYear("created"))
                .values("year")
                .annotate(num_posts=Count("id"))
                .order_by("-year")
        )
        return context


class TagView(BlogListView):

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(
                published=True,
                tags__slug=self.kwargs["slug"],
            )
            .prefetch_related("tags")
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tagview"] = self.kwargs["slug"]
        return context


class BlogYearView(BlogListView):

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(
                published=True,
                created__year=self.kwargs["year"],
            )
            .prefetch_related("tags")
            .order_by("-created")
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["yearview"] = self.kwargs["year"]
        return context

        
class BlogPostView(DetailView):
    model = BlogPost    
    template_name = "blog/post_detail.html"
    context_object_name = "post"

