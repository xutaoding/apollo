# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from django import conf
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apollo.settings.settings")

app = Celery('apollo_celery_app')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
# celery_app.autodiscover_tasks(lambda: conf.settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
