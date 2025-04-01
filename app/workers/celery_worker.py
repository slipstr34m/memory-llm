# celery_worker.py
from celery import Celery
from app.config import REDIS_URL

celery_app = Celery("user_profile_service", broker=REDIS_URL)

celery_app.conf.update(
    result_backend=REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)
