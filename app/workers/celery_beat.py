# app/workers/celery_beat.py
from celery import Celery
from app.workers.tasks import process_new_interviews
from app.config import REDIS_URL

celery_app = Celery("user_profile_service", broker=REDIS_URL)

celery_app.conf.beat_schedule = {
    "poll-interviews-every-minute": {
        "task": "app.workers.tasks.process_new_interviews",
        "schedule": 60.0,
        "args": (),
    },
}
