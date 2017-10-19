# -*- coding: utf-8 -*-

# Production Env Configure

import os
import sys
from os.path import dirname, abspath

import django
from django.core.handlers.wsgi import WSGIHandler

sys.path.append(dirname(dirname(abspath(__file__))))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'apollo.settings.prd')
django.setup()
application = WSGIHandler()
