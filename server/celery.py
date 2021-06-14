import os
from datetime import datetime

from celery import Celery, Task

Task.apply_async
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def plot_graph(func: str,
               interval: int,
               step: int,
               datetime: datetime = datetime.now):
    print(func, interval, step, datetime)
    return [[1, 2]]