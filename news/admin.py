from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'source', 'published_at')
    list_filter = ('category', 'source', 'published_at')
    search_fields = ('title', 'content', 'ai_summary')
