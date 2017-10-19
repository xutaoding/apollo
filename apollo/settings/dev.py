# -*- coding: utf-8 -*-

# Development Env Configure

# -*- coding: utf-8 -*-

# Production Env Configure

from settings import *

WSGI_APPLICATION = 'apollo.wsgi.wsgi.application'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
        'HOST': '192.168.216.172',
        'PORT': '3306'
    },
})

MONGODB = {
    'default': {
        'db': 'aegis',
        'host': '127.0.0.1',
        'port': 27017,
    }
}
