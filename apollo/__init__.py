from __future__ import absolute_import, unicode_literals

# from apollo.celery import app as celery_app  # Deprecated
from elastic_jobs.celery_app.celery import app as celery_app

__all__ = ['celery_app']

