# NewsSphere - GlobalNews Portal

A professional, scalable Django-based news portal with AI-powered features.

## Features
- **Professional Architecture**: Built with Django 6.0 and environment variable support.
- **Dynamic Content**: Article listings, detail views, and category filtering.
- **Premium Design**: Modern UI with a dedicated news layout, responsive navigation, and smooth animations.
- **AI-Ready**: Model includes fields for AI summaries and simplified content.
- **Production Scaling**: Pre-configured with WhiteNoise for static file serving.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML5, Vanilla CSS3 (Professional design)
- **Database**: SQLite (Development)
- **Scaling**: django-environ, WhiteNoise, Pillow

## Getting Started
1. Clone the repository.
2. Install dependencies: `pip install django django-environ Pillow whitenoise`
3. Set up your `.env` file (see `.env.example`).
4. Run migrations: `python manage.py migrate`
5. (Optional) Populate sample data: `python scripts/populate_news.py`
6. Run server: `python manage.py runserver`
