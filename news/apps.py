from django.apps import AppConfig
import os


class NewsConfig(AppConfig):
    name = 'news'

    def ready(self):
        import news.signals

        # Only start the scheduler in the main process (not in Django's reloader child process)
        # RUN_MAIN is set by Django's autoreloader for the child process
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                from news.scheduler import start
                start()
            except Exception as e:
                # Catching all exceptions to prevent the server from failing to start
                # (e.g. database table not created yet)
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Could not start scheduler: {e}")
