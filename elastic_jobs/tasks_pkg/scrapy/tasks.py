# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from scrapyd_api import ScrapydAPI

from elastic_jobs.settings import config


class ScrapyTasks(object):
    def __init__(self):
        self._scrapyd = ScrapydAPI(config.SCRAPYD_HOST)

    def launch_spider(self, project, spider):
        jobid = self._scrapyd.schedule(project, spider)
        return jobid


@shared_task
def add(x, y):
    return x + y

