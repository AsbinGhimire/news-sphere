from django.urls import path
from . import views

urlpatterns = [
    # Main Landing Page
    path('', views.HomeView.as_view(), name='index'),
    
    # Specific Article Details (SEO friendly slugs)
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Lists of articles by category (Nepal, World, Tech, etc.)
    path('category/<str:category_name>/', views.CategoryListView.as_view(), name='category_view'),
    
    # Global Search Page
    path('search/', views.ArticleSearchView.as_view(), name='search_view'),
    
    # Newsletter Subscription Handler
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # Static Information Pages
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('ethics/', views.EthicsView.as_view(), name='ethics'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
]
