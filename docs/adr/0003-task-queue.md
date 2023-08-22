# Task Queue

In the context of the task queue, I decided to use Celery agains Python RQ to easly implement a scheduled task in situations where it's not possible to configure cron jobs, implementing a retry policy and creation of task modules that can be reused to achieve fault tolerance accepting that Celery is more expensive solution.

## Considered Options

### Celery
Good, Periodic Tasks
Good, Async tasks
Good, Native support to retry failed tasks
Good, Extensive broker support
Good, Subtask support
Good, Modulerizations of tasks and their domain for reusability
Bad, Lack of user support

### Python RQ
Good, Supports async tasks
Bad, Only supports Redis
Bad, No subtask support

## Links
[Python RQ](https://python-rq.org/)
[Celery: Periodic Tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
