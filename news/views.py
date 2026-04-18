from django.shortcuts import render, get_object_or_404
from .models import Article

from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Article

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(ListView):
    model = Article
    template_name = 'news/index.html'
    context_object_name = 'latest_articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(published_at__isnull=False).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_articles = Article.objects.filter(published_at__isnull=False).order_by('-published_at')
        
        context['featured_article'] = all_articles.first()
        context['side_articles'] = all_articles[1:6]  # 5 articles for the hero sidebar
        
        # Categorized Sections
        context['world_news'] = Article.objects.filter(category='World').order_by('-published_at')[:4]
        context['tech_news'] = Article.objects.filter(category='Tech').order_by('-published_at')[:4]
        context['sports_news'] = Article.objects.filter(category='Sports').order_by('-published_at')[:4]
        
        context['categories'] = Article.CATEGORY_CHOICES
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryListView(ListView):
    model = Article
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category_name = self.kwargs['category_name']
        return Article.objects.filter(category=self.category_name).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category_name
        return context

class ArticleSearchView(ListView):
    model = Article
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 10

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
