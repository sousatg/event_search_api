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
    'add-every-30-seconds': {
        'task': 'worker.tasks.add',
        'schedule': 50.0
    },
}

app.conf.timezone = 'UTC'


@worker_ready.connect
def at_start(sender, **kwargs):
    """Run tasks at startup"""
    with sender.app.connection() as conn:
        sender.app.send_task(
            "worker.tasks.add",
            connection=conn
        )


if __name__ == '__main__':
    app.start()
