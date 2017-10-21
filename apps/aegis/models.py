# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from mongoengine import *

connect(alias='default', **settings.MONGODB['default'])


# Create your models here.
class BaseSQLModel(models.Model):
    username = models.CharField(max_length=20)
    crt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-crt']


class BaseDocument(DynamicDocument):
    crt = DateTimeField(default=datetime.now)

    meta = {
        'abstract': True,
        'ordering': ['-crt'],
        'allow_inheritance': True
    }


class SpiderTasksModel(BaseSQLModel):
    spider_name = models.CharField(max_length=126)
    spider_task_id = models.UUIDField()
    spider_description = models.CharField(max_length=1024)

    # Scrapy Basic Configure
    robotstxt_obey = models.BooleanField(default=True)
    cookies_enabled = models.BooleanField(default=True)
    download_delay = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    concurrent_requests = models.IntegerField(default=16)
    other_configure = models.TextField(default='{}')

    request_method = models.CharField(max_length=8, default='GET')
    request_cookies = models.TextField()
    request_headers = models.TextField()

    proxy_ip_enabled = models.BooleanField(default=False)
    login_username = models.CharField(max_length=32)
    login_password = models.CharField(max_length=128)

    class Meta:
        db_table = 'aegis_spider_tasks'


class MiddleFileModel(BaseSQLModel):
    FILE_UTILITY = (
        ('HT', 'Html'),
        ('PM', 'Parameter'),
    )

    spider_task_id = models.UUIDField()
    url = models.URLField(max_length=256)
    filename = models.CharField(max_length=128, unique=True)
    ext = models.CharField(max_length=8, default='.html')
    file_utility = models.CharField(max_length=2, choices=FILE_UTILITY)

    class Meta:
        db_table = 'aegis_middle_file'


class WalletModel(BaseSQLModel):
    PAY_MODE = (
        ('WX', 'WeChat'),
        ('AP', 'Alipay'),
    )

    pay_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    pay_mode = models.CharField(max_length=2, choices=PAY_MODE)
    pages_amount = models.IntegerField(default=150)

    class Meta:
        db_table = 'aegis_wallet'


class ConsumerRecordsMode(BaseSQLModel):
    spider_task_id = models.UUIDField()
    consumer_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    used_pages_amount = models.IntegerField(default=0)

    class Meta:
        db_table = 'aegis_consumer_records'


class ProxyIPDocument(BaseDocument):
    scheme = StringField(max_length=5)
    ip = StringField(max_length=15)
    port = StringField(max_length=8)

    meta = {
        'collection': 'aegis_proxy_ip'
    }


class SpiderTasksResultDocument(BaseDocument):
    spider_task_id = UUIDField()
    result = DynamicField()
    # result = DynamicEmbeddedDocument

    meta = {
        'collection': 'aegis_spider_tasks_result'
    }
