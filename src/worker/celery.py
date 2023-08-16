from celery import Celery
from celery.signals import worker_ready

app = Celery(
    'worker',
    broker='pyamqp://guest@localhost//',
    include=['worker.tasks']
)

app.conf.update(
    result_expires=3600,
)

app.conf.beat_schedule = {
    'extract-every-12-hours': {
        'task': 'worker.tasks.extract',
        'schedule': 12 * 60 * 60
    },
}

app.conf.timezone = 'UTC'


@worker_ready.connect
def at_start(sender, **kwargs):
    """Run tasks at startup"""
    with sender.app.connection() as conn:
        sender.app.send_task(
            "worker.tasks.extract",
            connection=conn
        )


if __name__ == '__main__':
    app.start()
