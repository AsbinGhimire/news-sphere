from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('World', 'World'),
        ('Tech', 'Tech'),
        ('Sports', 'Sports'),
        ('Health', 'Health'),
        ('Business', 'Business'),
    ]

    title = models.CharField(max_length=255, default='')
    description = models.TextField(null=True, blank=True, default='')
    content = models.TextField(null=True, blank=True, default='')
    source = models.CharField(max_length=200, null=True, blank=True, default='')
    author = models.CharField(max_length=100, null=True, blank=True, default='')
    image_url = models.URLField(max_length=500, null=True, blank=True, default='')
    published_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='World')
    article_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    ai_summary = models.TextField(blank=True, default='')
    paraphrased_content = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']
