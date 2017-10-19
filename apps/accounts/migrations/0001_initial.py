# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailVerifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crt', models.DateTimeField(auto_now=True)),
                ('verify_code', models.CharField(max_length=20)),
                ('owner_name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['-crt'],
                'db_table': 'mail_verify_code',
            },
        ),
    ]
