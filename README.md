# Celery Beat Scheduler Template

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/fastapi-celery-beat-worker-flower?referralCode=5oF91f&utm_medium=integration&utm_source=template&utm_campaign=generic)

Production-ready Celery Beat scheduler with flexible cron configuration and Railway deployment support.

## Example Scheduled Tasks

### 1. Every Minute

Runs every minute for frequent monitoring

```python
schedule: crontab(minute="*/1")
```

### 2. Hourly

Runs every hour at minute 0

```python
schedule: crontab(minute=0, hour="*")
```

### 3. Daily at Midnight

Runs once per day at 00:00

```python
schedule: crontab(minute=0, hour=0)
```

### 4. Twice Daily

Runs at 00:00 and 12:00 (configurable)

```python
schedule: crontab(minute=0, hour="0,12")
```

### 5. Weekly

Runs every Monday at 9 AM

```python
schedule: crontab(minute=0, hour=9, day_of_week=1)
```

### 6. Every 5 Minutes

Runs every 5 minutes

```python
schedule: crontab(minute="*/5")
```

### Deploy with API and Worker

For full functionality, deploy all three templates:

1. [FastAPI template](https://github.com/rubenszinho/celery-worker) (triggers tasks)
2. [Celery Worker template](https://github.com/rubenszinho/celery-worker) (processes tasks)
3. This Celery Beat template

All should share the same Redis instance via `${{Redis.REDIS_URL}}`.

## Adding Custom Scheduled Tasks

### Step 1: Define the Task

Edit `app/tasks.py`:

```python
@celery_app.task(name="your_scheduled_task")
def your_scheduled_task():
    """Your custom scheduled task logic"""
    # Your logic here
    return {"status": "completed"}
```

### Step 2: Add to Schedule

Edit `app/celery_config.py`:

```python
celery_app.conf.beat_schedule = {
    "your-task-name": {
        "task": "your_scheduled_task",
        "schedule": crontab(minute=0, hour="*/6"),  # Every 6 hours
    },
    # ... existing tasks
}
```

## Cron Schedule Examples

### Every 15 Minutes

```python
crontab(minute="*/15")
```

### Every Day at 3 AM

```python
crontab(minute=0, hour=3)
```

### Every Monday and Friday at 9 AM

```python
crontab(minute=0, hour=9, day_of_week="1,5")
```

### First Day of Every Month

```python
crontab(minute=0, hour=0, day_of_month=1)
```

### Every Weekday at 8 AM

```python
crontab(minute=0, hour=8, day_of_week="1-5")
```

### Every Quarter Hour

```python
crontab(minute="0,15,30,45")
```

## Monitoring

### Check Beat Status

```bash
# Check if beat is running
ps aux | grep "celery.*beat"

# Check logs
docker-compose logs beat
```

### Verify Schedule

```python
from app.celery_config import celery_app

schedule = celery_app.conf.beat_schedule
for name, config in schedule.items():
    print(f"{name}: {config['schedule']}")
```

## Common Use Cases

Daily reports, data synchronization, database cleanup, cache warming, backups, monitoring, batch processing.

## Configuration

### Dynamic Schedule

Load schedule from database or config file:

```python
def get_dynamic_schedule():
    # Load from database
    schedule = {}
    tasks = Task.query.filter_by(enabled=True).all()
    for task in tasks:
        schedule[task.name] = {
            "task": task.task_name,
            "schedule": crontab(**task.cron_config)
        }
    return schedule

celery_app.conf.beat_schedule = get_dynamic_schedule()
```

### Multiple Schedules

Different schedules for different environments:

```python
if settings.environment == "production":
    schedule = production_schedule
else:
    schedule = development_schedule

celery_app.conf.beat_schedule = schedule
```

## Troubleshooting

### Beat not starting

```bash
# Check Redis connection
redis-cli -u $REDIS_URL ping

# Check beat logs
docker-compose logs beat

# Verify schedule is loaded
celery -A beat.celery_app inspect scheduled
```

### Tasks not executing

```bash
# Ensure worker is running
celery -A worker.celery_app status

# Check if tasks are registered
celery -A worker.celery_app inspect registered

# Check beat logs for scheduling
docker-compose logs -f beat
```

### Schedule not updating

```bash
# Beat uses a schedule file (celerybeat-schedule)
# Delete it to force reload
rm celerybeat-schedule

# Restart beat
docker-compose restart beat
```

## Production Checklist

Set schedules, configure timezone, monitoring, Redis password, test in staging.

## Best Practices

Keep tasks idempotent, use appropriate intervals, monitor execution, set timeouts, log extensively.

## License

GPL-3.0
