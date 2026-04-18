from django.shortcuts import render, get_object_or_404
from .models import Article

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Article

class HomeView(ListView):
    model = Article
    template_name = 'news/index.html'
    context_object_name = 'latest_articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.filter(published_at__isnull=False).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_articles = self.get_queryset()
        context['featured_article'] = all_articles.first()
        # Ensure latest_articles in the context starts from the 2nd article
        context['latest_articles'] = all_articles[1:]
        context['categories'] = Article.CATEGORY_CHOICES
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

class CategoryListView(ListView):
    model = Article
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        self.category_name = self.kwargs['category_name']
        return Article.objects.filter(category=self.category_name).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category_name
        return context

class ArticleSearchView(ListView):
    model = Article
    template_name = 'news/category.html'  # Reusing category grid layout
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(content__icontains=query)
            ).order_by('-published_at')
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = f"Search Results for '{self.request.GET.get('q', '')}'"
        return context
