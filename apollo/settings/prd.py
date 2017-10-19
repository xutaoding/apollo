# -*- coding: utf-8 -*-

# Production Env Configure

from settings import *

WSGI_APPLICATION = 'apollo.wsgi.django_wsgi.application'

DATABASES.update({
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_00',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    },

    'apollo': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apollo_00',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '192.168.216.170',
        'PORT': '3306'
    },
})
