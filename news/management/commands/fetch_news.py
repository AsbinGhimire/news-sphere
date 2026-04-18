import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from news.models import Article
import os
import environ

class Command(BaseCommand):
    help = 'Fetches latest world news from NewsData.io API'

    def handle(self, *args, **options):
        # Ensure we have the latest env vars
        env = environ.Env()
        api_key = os.getenv('NEWSDATA_API_KEY')

        if not api_key or api_key == 'your_api_key_here':
            self.stdout.write(self.style.ERROR('API Key not found or still set to placeholder in .env'))
            self.stdout.write(self.style.WARNING('Please get a free key from https://newsdata.io/ and update your .env file.'))
            return

        url = f"https://newsdata.io/api/1/latest?apikey={api_key}&category=world&language=en"

        self.stdout.write(self.style.SUCCESS(f"Fetching news from {url}..."))

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'error':
                message = data.get('results', {}).get('message', 'Unknown API Error')
                self.stdout.write(self.style.ERROR(f"API Error: {message}"))
                return

            articles_added = 0
            results = data.get('results', [])

            for item in results:
                # NewsData.io specific fields
                title = item.get('title', 'No Title')
                article_id = item.get('article_id')
                description = item.get('description', '')
                content = item.get('content', '')
                source = item.get('source_id', 'Unknown')
                author = item.get('creator', ['Unknown'])[0] if item.get('creator') else 'Unknown'
                image_url = item.get('image_url', '')
                pub_date_str = item.get('pubDate')

                # Parse publication date
                published_at = parse_datetime(pub_date_str) if pub_date_str else None
                
                # article_id is our unique identifier to avoid duplicates
                obj, created = Article.objects.update_or_create(
                    article_id=article_id,
                    defaults={
                        'title': title,
                        'description': description,
                        'content': content,
                        'source': source,
                        'author': author,
                        'image_url': image_url,
                        'published_at': published_at,
                        'category': 'World',
                    }
                )

                if created:
                    articles_added += 1
                    self.stdout.write(self.style.SUCCESS(f"Successfully added: {title}"))

            self.stdout.write(self.style.SUCCESS(f"Finished! Added {articles_added} new articles."))

        except requests.exceptions.HTTPError as e:
            self.stdout.write(self.style.ERROR(f"HTTP Error: {e}"))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Request Error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
