import feedparser
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from news.models import Article
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'Fetches latest news about Nepal from Google News RSS'

    def handle(self, *args, **options):
        # RSS URL for Nepal News (Nepali Language & Region)
        url = "https://news.google.com/rss/search?q=Nepal&hl=ne&gl=NP&ceid=NP:ne"

        self.stdout.write(self.style.SUCCESS(f"Fetching news from {url}..."))

        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                self.stdout.write(self.style.ERROR(f"Error parsing feed: {feed.bozo_exception}"))
                return

            articles_added = 0
            
            for entry in feed.entries:
                # Basic Mapping
                title = entry.get('title', 'No Title')
                article_id = entry.get('id', entry.get('link'))
                link = entry.get('link', '')
                description = entry.get('summary', '')
                source = entry.get('source', {}).get('title', 'Google News')
                
                # Handling published date
                published_at = None
                if hasattr(entry, 'published_parsed'):
                    # Convert time_struct to aware datetime
                    dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    published_at = make_aware(dt)

                # article_id is our unique identifier to avoid duplicates
                obj, created = Article.objects.update_or_create(
                    article_id=article_id,
                    defaults={
                        'title': title,
                        'description': description,
                        'content': description, # RSS often only gives summary
                        'source': source,
                        'author': source,
                        'image_url': '', # Google News RSS doesn't directly provide high-res URLs
                        'published_at': published_at,
                        'category': 'Nepal',
                    }
                )

                if created:
                    articles_added += 1
                    # Safely handle console printing for characters like '\u0131'
                    safe_title = title.encode('ascii', 'ignore').decode('ascii')
                    self.stdout.write(self.style.SUCCESS(f"Successfully added: {safe_title}"))

            self.stdout.write(self.style.SUCCESS(f"Finished! Added {articles_added} new articles."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
