from django.db import models
from django.utils import timezone

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('World', 'World'),
        ('Tech', 'Tech'),
        ('Sports', 'Sports'),
        ('Health', 'Health'),
        ('Business', 'Business'),
    ]

    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    content = models.TextField(default='')
    source = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=100, null=True, blank=True, default='')
    image_url = models.URLField(max_length=500, default='')
    published_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='World')
    ai_summary = models.TextField(blank=True, default='')
    paraphrased_content = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']
