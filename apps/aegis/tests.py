# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests


# Create your tests here.
# url = 'http://127.0.0.1:8000/api/aegis/html_file/create'
url = 'http://192.168.216.172:8000/api/aegis/aegis/payment'
t_url = 'http://192.168.216.172:8000/api/account/token/obtain'
t_r = requests.post(t_url, data={'username': 'aegis', 'password': 'Abcd1234'})
token = t_r.json()['token']
cookie = t_r.cookies
print token
print dir(cookie)
print cookie.items()

# print requests.post(url, data={'username': 'admin', 'url': 'http://www.bbb.com/aaa.html'}).content
print requests.get(url, headers={'Authorization': 'JWT-MSC ' + token}).content

