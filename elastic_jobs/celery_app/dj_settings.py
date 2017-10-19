# -*- coding: utf-8 -*-

# 建议：该配置文件最好仅于celery相关的配置，其他的配置可用于文件.

DJ_CELERY_BROKER_URL = 'amqp://dingxutao:dingxutao@192.168.216.171:5672//celery_scrapy'
DJ_CELERY_RESULT_BACKEND = 'redis://192.168.216.171:6379/1'
DJ_CELERY_TASK_RESULT_EXPIRES = 60

DJ_CELERY_ACCEPT_CONTENT = ['json', ]
DJ_CELERY_TASK_SERIALIZER = 'json'
DJ_CELERY_RESULT_SERIALIZER = 'json'

DJ_CELERY_DEFAULT_EXCHANGE = 'scrapy_exchange'
DJ_CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'

