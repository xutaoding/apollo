# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class MailVerifyCode(models.Model):
    crt = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    verify_code = models.CharField(max_length=20)
    owner_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'mail_validation_code'
        ordering = ['-crt']

