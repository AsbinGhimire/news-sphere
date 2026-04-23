from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Article(models.Model):
    """
    Represents a news article in the system.
    Stores content, metadata, and AI-generated enhancements.
    """
    CATEGORY_CHOICES = [
        ('Nepal', 'Nepal'),
        ('World', 'World'),
        ('Tech', 'Tech'),
        ('Sports', 'Sports'),
        ('Health', 'Health'),
        ('Business', 'Business'),
    ]

    # Core Content
    title = models.CharField(max_length=255, default='', help_text="The headline of the article.")
    description = models.TextField(null=True, blank=True, default='', help_text="A brief summary for previews.")
    content = models.TextField(null=True, blank=True, default='', help_text="The full HTML or text content of the news.")
    
    # Metadata & Attribution
    source = models.CharField(max_length=200, null=True, blank=True, default='', help_text="Original source (e.g., Google News).")
    author = models.CharField(max_length=100, null=True, blank=True, default='', help_text="Name of the writer.")
    image_url = models.URLField(max_length=500, null=True, blank=True, default='', help_text="Path to the featured image.")
    published_at = models.DateTimeField(default=timezone.now, null=True, blank=True, help_text="Date the article was published.")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='World', help_text="News classification.")
    
    # Identifiers & SEO
    article_id = models.CharField(max_length=255, unique=True, null=True, blank=True, help_text="Unique external ID (e.g., from an API).")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, help_text="URL-friendly identifier generated from the title.")
    
    # AI-Generated Features
    ai_summary = models.TextField(blank=True, default='', help_text="Concise AI-generated summary.")
    paraphrased_content = models.TextField(blank=True, default='', help_text="Simplified version of the content for readability.")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to automatically generate a unique slug if not provided.
        Ensures SEO-friendly URLs.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness by appending a counter if needed
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def estimated_reading_time(self):
        """
        Calculates the estimated reading time in minutes.
        Assumes an average reading speed of 200 words per minute.
        """
        if not self.content:
            return 1
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class NewsletterSubscription(models.Model):
    """
    Stores email addresses of users who have subscribed to the newsletter.
    """
    email = models.EmailField(unique=True, help_text="Subscriber's email address.")
    active = models.BooleanField(default=True, help_text="Whether the subscription is currently active.")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
