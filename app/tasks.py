
import logging
from datetime import datetime
from typing import Any, Dict

from app.celery_config import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="scheduled_task")
def scheduled_task() -> Dict[str, Any]:
    """Main scheduled task triggered by BEAT_SCHEDULE_CRON environment variable."""
    logger.info("Running scheduled task")

    current_time = datetime.utcnow()

    # Add your task logic here

    return {
        "task": "scheduled_task",
        "executed_at": current_time.isoformat(),
        "status": "completed",
    }
