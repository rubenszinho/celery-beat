"""
Celery Beat Entrypoint

This script is the entry point for starting the Celery Beat scheduler.
"""

from app.celery_config import celery_app

# Import tasks to register them with Celery
from app.tasks import (
    cleanup_old_results,
    scheduled_task_daily,
    scheduled_task_every_minute,
    scheduled_task_frequent,
    scheduled_task_hourly,
    scheduled_task_twice_daily,
    scheduled_task_weekly,
    send_notifications,
)

if __name__ == "__main__":
    celery_app.start()
