from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.BlogListView.as_view(), name="list"),
    path("tag/<slug:slug>/", views.TagView.as_view(), name="tag"),
    path("archive/<int:year>/", views.BlogYearView.as_view(), name="year"),
    path("<slug:slug>", views.BlogPostView.as_view(), name="post"),
    path("<slug:slug>.md", views.post_source, name="source"),
    path("<slug:slug>/discuss", views.discuss, name="discuss"),
]

