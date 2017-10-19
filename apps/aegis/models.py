# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from django.conf import settings
# from mongoengine import *

# connect(alias='default', **settings.MONGODB['default'])


# Create your models here.
class AegisFileModel(models.Model):
    username = models.CharField(max_length=20)
    url = models.URLField(max_length=256)
    fn_md5 = models.CharField(max_length=128, unique=True)
    ext = models.CharField(max_length=8, default='.html')
    crt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aegis_file'
        ordering = ['-crt']






