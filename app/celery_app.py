from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=['app.tasks.background_tasks']
)

celery_app.conf.beat_schedule = {
    "fetch-crypto-prices-every-minute": {
        "task": "app.tasks.background_tasks.fetch_prices_task",
        "schedule": crontab(minute="*"),
    },
}
celery_app.conf.timezone = "UTC"