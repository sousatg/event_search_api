from celery import Celery
from celery.signals import worker_ready
from config.celery_config import CeleryConfig


app = Celery(
    'worker',
    include=['worker.tasks']
)

app.config_from_object(CeleryConfig)


@worker_ready.connect
def at_start(sender, **kwargs):
    '''Run tasks at startup'''
    with sender.app.connection() as conn:
        sender.app.send_task(
            'worker.tasks.extract',
            connection=conn
        )


if __name__ == '__main__':
    app.start()
