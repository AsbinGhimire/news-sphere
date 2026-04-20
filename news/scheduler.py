import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django import db

logger = logging.getLogger(__name__)


def fetch_news_job():
    """
    Runs the fetch_news management command as a scheduled job.
    This will pull the latest Nepal news from Google News RSS
    and update the database automatically.
    """
    logger.info("⏰ Scheduled job: Starting automatic news fetch...")

    try:
        from django.core.management import call_command
        call_command("fetch_news")
        logger.info("✅ Scheduled news fetch completed successfully.")
    except Exception as e:
        logger.error(f"❌ Scheduled news fetch failed: {e}")
    finally:
        # Close old DB connections to prevent stale connection errors
        db.close_old_connections()


def delete_old_job_executions(max_age_seconds=604_800):
    """
    Deletes APScheduler job execution entries older than 7 days (604800 seconds).
    Keeps the job execution log clean and prevents database bloat.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age_seconds)


def start():
    """
    Starts the APScheduler background scheduler.
    - Fetches news every day at 6:00 AM (Nepal time: UTC+05:45 = 00:15 UTC).
    - Also fetches news 3 more times per day (every 6 hours) for freshness.
    - Cleans up old execution logs weekly.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # --- Fetch news every 6 hours (4 times/day for freshness) ---
    scheduler.add_job(
        fetch_news_job,
        trigger=CronTrigger(hour="*/6", minute="0"),  # 00:00, 06:00, 12:00, 18:00 UTC
        id="fetch_news_every_6_hours",
        name="Fetch Nepal News Every 6 Hours",
        jobstore="default",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=300,  # 5 min grace window if server was briefly down
    )

    # --- Clean up old job executions every Sunday at midnight ---
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

    logger.info("🚀 APScheduler started. News will be fetched automatically every 6 hours.")
    scheduler.start()
