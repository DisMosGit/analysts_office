import os
import io
from datetime import datetime, timedelta
from time import mktime
from typing import Union

from numpy import *

import matplotlib.pyplot as plt
from celery import Celery, Task
from django.core.files.storage import default_storage

Task.apply_async
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def get_unix(dt: datetime, delta: int = None):
    if delta:
        return mktime((dt - timedelta(days=delta)).timetuple())
    else:
        return mktime(dt.timetuple())


def get_t(dt: Union[str, datetime], delta: int = None):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(get_unix(dt, delta))
    return get_unix(dt, delta) / (60 * 60)


@app.task
def plot_graph_by_data(func: str,
                       interval: int,
                       step: int,
                       time_end: datetime = datetime.now):
    t: ndarray = arange(
        get_t(time_end, interval),
        get_t(time_end),
        step,
    )
    y: ndarray = eval(func)
    figure = io.BytesIO()
    # print(t, y)
    plt.plot(
        t,
        y,
        color=random.random(3),
        linewidth=3,
        marker='',
    )
    plt.savefig(figure, format="png", dpi=300, transparent=True)
    file_path = default_storage.save(
        f"plot.png",
        figure,
    )
    return file_path
