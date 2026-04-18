import os
import django
import sys
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GlobalNews.settings')
django.setup()

from news.models import Article

def populate():
    print("Clearing existing articles...")
    Article.objects.all().delete()

    sample_articles = [
        {
            'title': 'The Future of AI: Generative Models Take Center Stage',
            'category': 'Tech',
            'source': 'TechDaily',
            'author': 'Alex Rivers',
            'image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1000',
            'description': 'Exploring how generative AI is transforming industries from software development to creative arts.',
            'content': 'Artificial Intelligence has seen a massive surge in capability with the advent of large-scale generative models. These systems, trained on diverse datasets, can now produce human-like text, intricate images, and even functional code. Experts predict that within the next five years, AI-augmented workflows will be the standard across all professional sectors.',
            'ai_summary': '• Generative AI is rapidly evolving and moving into mainstream professional workflows.\n• Transformation is occurring in both technical and creative fields.\n• Expectations of AI-augmented standards within 5 years.',
            'paraphrased_content': 'AI is getting smarter and starting to help people with their jobs everywhere. Soon, using AI at work will be as normal as using a computer is today.',
            'published_at': timezone.now() - timedelta(hours=2)
        },
        {
            'title': 'Global Economic Outlook: Stability Amidst Volatility',
            'category': 'Business',
            'source': 'FinanceGlobal',
            'author': 'Sarah Chen',
            'image_url': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=1000',
            'description': 'Leading economists discuss the surprising resilience of global markets in the face of shifting trade policies.',
            'content': 'Despite previous forecasts of a significant slowdown, the global economy has shown remarkable resilience. Consumer spending remains robust, and core inflation is beginning to stabilize in key European and North American markets. However, geopolitical tensions continue to present a risk factor for long-term supply chain stability.',
            'ai_summary': '• Global economy is performing better than predicted by economists.\n• Stability is returning to inflation rates in major markets.\n• Supply chains remain vulnerable to geopolitical shifts.',
            'paraphrased_content': 'The world economy is doing okay for now, which is a nice surprise. Prices are stopping their fast climb, but there are still things to worry about in international trade.',
            'published_at': timezone.now() - timedelta(hours=5)
        },
        {
            'title': 'Breakthrough in Sustainable Energy: Fusion Milestone Reached',
            'category': 'World',
            'source': 'ScienceMonitor',
            'author': 'Dr. Julian Thorne',
            'image_url': 'https://images.unsplash.com/photo-1509391366360-fe5bb58583bb?auto=format&fit=crop&q=80&w=1000',
            'description': 'International research team achieves sustained net energy gain in a compact fusion reactor design.',
            'content': 'A team of physicists at the International Fusion Center has announced a major breakthrough. Their latest experiment successfully maintained a net energy gain for over thirty minutes, a new world record. This brings us one step closer to the dream of clean, limitless energy for the entire planet.',
            'ai_summary': '• New record for sustained energy gain in fusion research.\n• Milestone achieved by an international collaborative team.\n• Potential for a future with clean, unlimited power.',
            'paraphrased_content': 'Scientists found a way to get more energy out of a machine than they put in, for a long time! This is a big step toward having power that never runs out and doesn\'t hurt the environment.',
            'published_at': timezone.now() - timedelta(days=1)
        },
        {
            'title': 'Summer Olympics 2026: Host City Preparations Peak',
            'category': 'Sports',
            'source': 'SportsWire',
            'author': 'Marcus Webb',
            'image_url': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&q=80&w=1000',
            'description': 'New eco-friendly stadium designs are completed as the city gears up for the largest sporting event in history.',
            'content': 'The infrastructure for the 2026 Summer Games is nearly 90% complete. The organizing committee highlighted the use of recycled materials in the construction of the primary athletes\' village. Tourism is expected to bring a record-breaking 3 million visitors to the region.',
            'ai_summary': '• 2026 Olympics infrastructure is nearing completion.\n• Heavy focus on sustainability and eco-friendly construction.\n• Expected record visitor numbers for the host region.',
            'paraphrased_content': 'The city is almost ready for the big 2026 Olympics. They built everything to be good for the earth, and they are expecting more people to visit than ever before.',
            'published_at': timezone.now() - timedelta(hours=10)
        },
        {
            'title': 'New Wellness Trends: The Rise of Biophilic Living',
            'category': 'Health',
            'source': 'HealthLine',
            'author': 'Elena Martinez',
            'image_url': 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&q=80&w=1000',
            'description': 'How incorporating natural elements into home and workspace design is measurably reducing chronic stress.',
            'content': 'Recent studies published in the Journal of Environmental Health show that "biophilic" design—integrating plants, natural light, and organic textures—can reduce cortisol levels by up to 15%. Designers are now prioritizing green spaces even in high-density urban apartments.',
            'ai_summary': '• Biophilic design is proven to lower stress hormones like cortisol.\n• Increasing trend of bringing nature into urban architecture.\n• Measurable health benefits are driving high-end design shifts.',
            'paraphrased_content': 'Adding plants and sunlight to your home isn\'t just pretty—it actually helps you feel less stressed. Because of this, even city apartments are being designed to include more "green" stuff.',
            'published_at': timezone.now() - timedelta(days=2)
        }
    ]

    for data in sample_articles:
        Article.objects.create(**data)
        print(f"Created: {data['title']}")

    print("Population complete!")

if __name__ == '__main__':
    populate()
