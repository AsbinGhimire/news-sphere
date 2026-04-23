from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, NewsletterSubscription
from .utils import WeatherService

from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(ListView):
    """
    The main landing page of the portal.
    Displays a featured article (priority to Nepal news), 
    side headlines, and categorized sections.
    """
    model = Article
    template_name = 'news/index.html'
    context_object_name = 'latest_articles'
    paginate_by = 10

    def get_queryset(self):
        """Returns only published articles ordered by publication date."""
        return Article.objects.filter(published_at__isnull=False).order_by('-published_at')

    def get_context_data(self, **kwargs):
        """
        Extends context to include featured logic and categorized news sections.
        Implements high-priority Nepal news logic.
        """
        context = super().get_context_data(**kwargs)
        all_articles = Article.objects.filter(published_at__isnull=False).order_by('-published_at')
        
        # Priority 1: Nepal News Logic
        # We separate Nepal news to ensure it's front and center for our primary audience.
        nepal_news = all_articles.filter(category='Nepal')
        other_news = all_articles.exclude(category='Nepal')
        
        # Featured is always the latest Nepal story if available, otherwise latest from other categories.
        if nepal_news.exists():
            context['featured_article'] = nepal_news.first()
            # Side articles are the next 5 Nepal stories for local focus
            context['side_articles'] = nepal_news[1:6]
        else:
            context['featured_article'] = other_news.first()
            context['side_articles'] = other_news[1:6]
        
        # Categorized Sections for layout
        context['nepal_list'] = nepal_news[:4]
        context['world_news'] = all_articles.filter(category='World').order_by('-published_at')[:4]
        context['tech_news'] = Article.objects.filter(category='Tech').order_by('-published_at')[:4]
        context['sports_news'] = Article.objects.filter(category='Sports').order_by('-published_at')[:4]
        
        context['categories'] = Article.CATEGORY_CHOICES
        return context

class ArticleDetailView(DetailView):
    """
    Displays the full content of a single article.
    Includes related news from the same category.
    """
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Fetches up to 4 related articles excluding the current one."""
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['related_articles'] = Article.objects.filter(
            category=article.category
        ).exclude(id=article.id)[:4]
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryListView(ListView):
    """
    Lists articles belonging to a specific category.
    Accessed via category name in the URL.
    """
    model = Article
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        """Filters articles by the category name passed in the URL."""
        self.category_name = self.kwargs['category_name']
        return Article.objects.filter(category=self.category_name).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category_name
        return context

class ArticleSearchView(ListView):
    """
    Handles search functionality across title, description, and content.
    """
    model = Article
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        """Performs a search query if keyword 'q' is present in GET parameters."""
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


def subscribe_newsletter(request):
    """
    Handles newsletter subscription requests via POST.
    Supports both traditional form submissions and AJAX requests.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # Use get_or_create to avoid duplicate subscriptions
                obj, created = NewsletterSubscription.objects.get_or_create(email=email)
                status = 'success'
                if created:
                    message = "Thank you! You've successfully subscribed to our newsletter."
                else:
                    message = "You are already a subscriber. Thank you for your interest!"
            except Exception:
                status = 'error'
                message = "Something went wrong. Please try again."
        else:
            status = 'error'
            message = "Please provide a valid email address."

        # AJAX support for seamless UI experience
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'status': status, 'message': message})

        # Fallback for traditional form POST
        if status == 'success':
            messages.success(request, message)
        else:
            messages.error(request, message)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def global_context(request):
    """
    Global context processor.
    Injected into every template to provide global data like weather and year.
    """
    return {
        'weather': WeatherService.get_weather(),
        'current_year': 2026
    }

class AboutView(TemplateView):
    """Simple view for the static About page."""
    template_name = 'news/about.html'

class ContactView(TemplateView):
    """Simple view for the static Contact page."""
    template_name = 'news/contact.html'

class EthicsView(TemplateView):
    """Simple view for the Journalistic Ethics page."""
    template_name = 'news/ethics.html'

class PrivacyView(TemplateView):
    """Simple view for the Privacy Policy page."""
    template_name = 'news/privacy.html'

class TermsView(TemplateView):
    """Simple view for the Terms of Service page."""
    template_name = 'news/terms.html'
