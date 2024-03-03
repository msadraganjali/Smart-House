from . import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# class list kardan article
class ArticleListView(ListView):
    model = models.Article
    context_object_name = 'articles'
    template_name = 'blog/list.html'
    paginate_by = 4
    
    def get_queryset(self):
        return models.Article.objects.order_by('-updated', '-created').filter(status = 'p')

# class braye didan article
class ArticleDetailView(DetailView):
    model = models.Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    