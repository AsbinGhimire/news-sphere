import feedparser
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from news.models import Article
from datetime import datetime
import time
import re
import urllib.parse

class Command(BaseCommand):
    help = 'Fetches latest news about Nepal from Google News RSS with Smart Sanitization'

    def generate_smart_insight(self, title):
        """Generates a professional 2-3 line summary based on the headline."""
        clean_title = title.split(' - ')[0] if ' - ' in title else title
        return (f"This strategic update highlights major developments regarding '{clean_title}'. "
                f"GlobalDiscovery analysis suggests this event significantly impacts the current localized reporting landscape. "
                "Early indicators point to a shift in institutional focus within the region.")

    def generate_simple_words(self, title):
        """Generates a simplified, conversational version of the headline."""
        clean_title = title.split(' - ')[0] if ' - ' in title else title
        return f"In simple terms: People are currently discussing '{clean_title}' because of its high relevance to Nepal. It's an important story that's making headlines across several local sources today."

    def generate_image_prompt(self, title, category):
        """Generates a smart category-based image prompt for AI image generation."""
        category_prompts = {
            'Politics': 'Realistic photo of government officials, parliament discussion, press conference, serious tone, professional journalism photography, natural lighting, documentary style, 16:9',
            'Government': 'Realistic photo of government officials, parliament discussion, press conference, serious tone, professional journalism photography, natural lighting, documentary style, 16:9',
            'Sports': 'High-action sports photography, athletes in motion, stadium environment, dynamic but realistic, professional sports journalism style, sharp focus, 16:9',
            'Tech': 'Modern technology scene, developers working, AI concept, futuristic but realistic office environment, clean lighting, minimal aesthetic, editorial tech photography, 16:9',
            'Health': 'Medical professionals in hospital setting, patient care, clean environment, soft lighting, realistic healthcare photography, trustworthy tone, 16:9',
            'Business': 'Corporate environment, business meeting, finance discussion, city skyline, professional atmosphere, realistic editorial photography, 16:9',
        }
        
        # Default to General/Breaking News style if category not found
        category_style = category_prompts.get(category, 'Real-world event scene, people, environment, natural composition, journalistic storytelling image, neutral tone, professional news photography, 16:9')

        return f"""
Professional editorial news image for headline: "{title}"

Category: {category}
Scene Context: {category_style}

Realistic journalism photography style, BBC News style,
natural lighting, authentic scene, high detail,
16:9 aspect ratio, no text, no watermark
""".strip()

    def handle(self, *args, **options):
        # RSS URL for Nepal News (Nepali Language & Region)
        url = "https://news.google.com/rss/search?q=Nepal&hl=ne&gl=NP&ceid=NP:ne"

        self.stdout.write(self.style.SUCCESS(f"Connecting to GlobalDiscovery Intelligence Bridge: {url}"))

        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                self.stdout.write(self.style.ERROR(f"Error parsing feed: {feed.bozo_exception}"))
                return

            articles_added = 0
            
            for entry in feed.entries:
                # Basic Mapping
                raw_title = entry.get('title', 'No Title')
                article_id = entry.get('id', entry.get('link'))
                link = entry.get('link', '')
                raw_summary = entry.get('summary', '')
                
                # Precise Cleaning with BeautifulSoup
                soup = BeautifulSoup(raw_summary, "html.parser")
                clean_description = soup.get_text().strip()
                
                # Extract clean source and title
                source = entry.get('source', {}).get('title', 'Google News')
                if ' - ' in raw_title:
                    clean_title = raw_title.rsplit(' - ', 1)[0]
                else:
                    clean_title = raw_title

                # Smart Intelligence Generation
                category_name = 'Nepal'
                ai_summary = self.generate_smart_insight(clean_title)
                simple_words = self.generate_simple_words(clean_title)
                
                # AI Image Generation
                image_prompt = self.generate_image_prompt(clean_title, category_name)
                encoded_prompt = urllib.parse.quote(image_prompt)
                ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
                
                # Handling published date
                published_at = None
                if hasattr(entry, 'published_parsed'):
                    dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    published_at = make_aware(dt)

                # article_id is our unique identifier to avoid duplicates
                obj, created = Article.objects.update_or_create(
                    article_id=article_id,
                    defaults={
                        'title': clean_title,
                        'description': clean_description,
                        'content': clean_description,
                        'source': source,
                        'author': source,
                        'image_url': ai_image_url, 
                        'published_at': published_at,
                        'category': category_name,
                        'ai_summary': ai_summary,
                        'paraphrased_content': simple_words,
                    }
                )

                if created:
                    articles_added += 1
                    safe_title = clean_title.encode('ascii', 'ignore').decode('ascii')
                    self.stdout.write(self.style.SUCCESS(f"Successfully added & sanitized: {safe_title}"))
                else:
                    # Even if not created, let's update and clean existing bad data
                    obj.title = clean_title
                    obj.description = clean_description
                    obj.content = clean_description
                    obj.ai_summary = ai_summary
                    obj.paraphrased_content = simple_words
                    obj.image_url = ai_image_url
                    obj.save()

            self.stdout.write(self.style.SUCCESS(f"Finished Data Sanitized! Processed {len(feed.entries)} articles. Added {articles_added} new."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
