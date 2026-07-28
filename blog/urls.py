from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.BlogListView.as_view(), name="index"),
    path("<slug:slug>/", views.BlogPostView.as_view(), name="detail"),
    path("tag/<slug:slug>/", views.TagView.as_view(), name="tag"),
    path("<int:year>", views.BlogYearView.as_view(), name="year"),
    path("<slug:slug>.md", views.post_source, name="source"),
    path("<slug:slug>/discuss", views.discuss, name="discuss"),
]

