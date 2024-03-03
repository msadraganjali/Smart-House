from . import views
from django.urls import path, include
# address haye apilication blog
app_name = 'blog'
urlpatterns = [
    path("", views.ArticleListView.as_view() , name="list"),
    path("<slug:slug>", views.ArticleDetailView.as_view() , name="detail"),
]
