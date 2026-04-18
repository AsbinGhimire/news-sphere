from django.shortcuts import render, get_object_or_404
from .models import Article

def index(request):
    latest_articles = Article.objects.filter(published_at__isnull=False).order_by('-published_at')[:10]
    categories = Article.CATEGORY_CHOICES
    return render(request, 'news/index.html', {
        'latest_articles': latest_articles,
        'categories': categories
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'news/article_detail.html', {'article': article})

def category_view(request, category_name):
    articles = Article.objects.filter(category=category_name).order_by('-published_at')
    return render(request, 'news/category.html', {
        'articles': articles,
        'category_name': category_name
    })
