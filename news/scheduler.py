import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django import db

# Initialize logger for the scheduler
logger = logging.getLogger(__name__)


def fetch_news_job():
    """
    Background worker that runs the 'fetch_news' management command.
    Standardizes and pulls the latest Nepal news from external RSS feeds.
    Automatically handles database connections and error logging.
    """
    logger.info("⏰ Scheduled job: Starting automatic news fetch synchronization...")

    try:
        from django.core.management import call_command
        # Executes the custom management command defined in news/management/commands/fetch_news.py
        call_command("fetch_news")
        logger.info("✅ Scheduled news fetch completed successfully.")
    except Exception as e:
        logger.error(f"❌ Scheduled news fetch failed: {e}")
    finally:
        # Crucial for long-running processes: ensures DB connections are reset
        db.close_old_connections()


def delete_old_job_executions(max_age_seconds=604_800):
    """
    Maintenance task to prune old APScheduler job execution history.
    Keeps the 'django_apscheduler' tables lean and improves overall database performance.
    Default: deletes logs older than 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age_seconds)


def start():
    """
    Initialization point for the background process scheduler.
    Sets up the persistent job store and adds recurring tasks.
    
    Scheduled Tasks:
    1. Fresh News Fetch: Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC).
    2. Weekly Maintenance: Every Sunday at midnight to clean logs.
    """
    scheduler = BackgroundScheduler()
    # Uses the Django DB as the persistent store for job state
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # --- Fresh News Sync: 4 times a day ensures content remains current ---
    scheduler.add_job(
        fetch_news_job,
        trigger=CronTrigger(hour="*/6", minute="0"),  
        id="fetch_news_every_6_hours",
        name="Fetch Nepal News Every 6 Hours",
        jobstore="default",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=300,  # Grace period for server restarts
    )

    # --- Weekly Cleanup: Optimized maintenance schedule ---
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="sun", hour="0", minute="0"),
        id="delete_old_job_executions",
        name="Delete Old Job Executions (Weekly Cleanup)",
        jobstore="default",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=300,
    )

    logger.info("🚀 Background Scheduler Engine Started. Automated content sync is active.")
    scheduler.start()
