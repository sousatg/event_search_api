import os


class CeleryConfig:
    broker_url = os.environ.get("CELERY_BROKER_URL") or "pyamqp://guest@localhost//"

    beat_schedule = {
        "extract-every-12-hours": {
            "task": "worker.provider_scraper.tasks.process_fetch",
            "schedule": 12 * 60 * 60,  # 12 hours in seconds
        },
    }

    timezone = "UTC"
