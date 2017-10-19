# -*- coding: utf-8 -*-

# 建议：该配置文件最好仅于celery相关的配置，其他的配置可用于文件.

CELERY_BROKER_URL = 'amqp://dingxutao:dingxutao@192.168.216.172:5672//celery_scrapy'
# CELERY_RESULT_BACKEND = 'redis://192.168.216.171:6379/1'
# CELERY_TASK_RESULT_EXPIRES = 60

CELERY_RESULT_BACKEND = 'django-db'

CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_EXCHANGE = 'scrapy_exchange'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'

