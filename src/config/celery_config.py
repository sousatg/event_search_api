class CeleryConfig:
    broker_url = 'pyamqp://guest@localhost//'

    beat_schedule = {
        'extract-every-12-hours': {
            'task': 'worker.tasks.extract',
            'schedule': 12 * 60 * 60,  # 12 hours in seconds
        },
    }

    timezone = 'UTC'
