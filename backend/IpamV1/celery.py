# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from django.apps import apps
# set the default Django settings module for the 'celery' program.
from django.utils import timezone
from kombu import Queue, Exchange
from celery import Celery, platforms, Task
from celery_once import QueueOnce

from IpamV1 import settings

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IpamV1.settings')

app = Celery('IpamV1')

app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': settings.CELERY_ONCE_URL,
        'default_timeout': 60 * 60
    }
}
# app.conf.beat_schedule = {
#     # Disable cleanup task by scheduling to run every ~1000 years
#     'backend_cleanup': {
#         'task': 'celery.backend_cleanup',
#         'schedule': timedelta(days=365*1000),
#         'relative': True,
#     },
# }
app.now = timezone.now
app.config_from_object('django.conf:settings', namespace='CELERY')

default_exchange = Exchange('default', type='direct')
ipam_exchange = Exchange('ipam', type='direct')

app.conf.task_time_limit = 86400
app.conf.worker_prefetch_multiplier = 10
app.conf.worker_max_tasks_per_child = 100
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('ipam', ipam_exchange, routing_key='ipam'),
)
# app.backend.supports_autoexpire = True
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


class IpAmTask(QueueOnce):

    def run(self, *args, **kwargs):
        pass

    max_retries = 1
    autoretry_for = (Exception, KeyError, RuntimeError)
    retry_kwargs = {'max_retries': 1}
    retry_backoff = False

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(str(einfo))
        return super(IpAmTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # print('task retry, reason: {0}'.format(exc))
        print(str(einfo))
        return super(IpAmTask, self).on_failure(exc, task_id, args, kwargs, einfo)
