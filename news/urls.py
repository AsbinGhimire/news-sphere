from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/<str:category_name>/', views.CategoryListView.as_view(), name='category_view'),
    path('search/', views.ArticleSearchView.as_view(), name='search_view'),
]
