from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walnut.settings')

app = Celery('walnut')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

platforms.C_FORCE_ROOT = True


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sum-task': {
            'task': 'vpnstatus.tasks.get_vpn_status',
            'schedule': timedelta(seconds=60)
        }
    }
)
