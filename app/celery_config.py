
import logging

from app.config import settings
from celery import Celery
from celery.schedules import crontab

logger = logging.getLogger(__name__)


celery_app = Celery(
    "beat_scheduler",
    broker=settings.get_broker_url(),
    backend=settings.get_result_backend(),
    include=["app.tasks"],  
)


celery_app.conf.update(
    
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    result_expires=86400,  
    
    beat_max_loop_interval=5,  
)



def parse_cron_schedule(cron_string: str) -> dict:
    try:
        parts = cron_string.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron format: {cron_string}")

        minute, hour, day_of_month, month, day_of_week = parts

        return {
            "minute": minute,
            "hour": hour,
            "day_of_month": day_of_month,
            "month_of_year": month,
            "day_of_week": day_of_week,
        }
    except Exception as e:
        logger.error(f"Error parsing cron schedule '{cron_string}': {e}")
        
        return {
            "minute": "0",
            "hour": "0",
            "day_of_month": "*",
            "month_of_year": "*",
            "day_of_week": "*",
        }



cron_kwargs = parse_cron_schedule(settings.beat_schedule_cron)

celery_app.conf.beat_schedule = {
    
    "example-every-minute": {
        "task": "scheduled_task_every_minute",
        "schedule": crontab(minute="*/1"),
        "options": {
            "expires": 300,  
        },
    },
    
    "example-hourly": {
        "task": "scheduled_task_hourly",
        "schedule": crontab(minute=0, hour="*"),  
    },
    
    "example-daily-midnight": {
        "task": "scheduled_task_daily",
        "schedule": crontab(minute=0, hour=0),  
    },
    
    "example-twice-daily": {
        "task": "scheduled_task_twice_daily",
        "schedule": crontab(**cron_kwargs),  
    },
    
    "example-weekly-monday": {
        "task": "scheduled_task_weekly",
        "schedule": crontab(minute=0, hour=9, day_of_week=1),  
    },
    
    "example-every-5-minutes": {
        "task": "scheduled_task_frequent",
        "schedule": crontab(minute="*/5"),
    },
}

logger.info(f"Celery Beat configured with schedule: {settings.beat_schedule_cron}")
logger.info(f"Parsed cron: {cron_kwargs}")
