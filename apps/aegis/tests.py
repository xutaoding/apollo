# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests


# Create your tests here.
url = 'http://127.0.0.1:8000/api/aegis/html_file/create'
t_url = 'http://127.0.0.1:8000/api-auth/token/obtain'
# t_r = requests.post(t_url, data={'username': 'admin', 'password': 'admin123'})
# token = t_r.json()['token']
# cookie = t_r.cookies['drf-jwt-apollo']
# print token
# print cookie

print requests.post(url, data={'username': 'admin', 'url': 'http://www.bbb.com/aaa.html'}).content