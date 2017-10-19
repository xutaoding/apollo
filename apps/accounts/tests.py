# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
from django.test import TestCase

# Nothing
# from django.middleware.clickjacking import XFrameOptionsMiddleware
# from rest_framework_jwt.utils import jwt_response_payload_handler, jwt_decode_handler

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your tests here.

import requests

user = {
    'username': 'admin',
    'password': 'admin123'
}

# url = 'http://127.0.0.1:8000/api-auth/mail/send?aaaaa=100000'
url = 'http://192.168.216.171:8000/api-auth/mail/send?aaaaa=100000'
headers = {
    'Content-Type': 'application/json'
}
# r = requests.post(url, data=user)
# token = r.json()['token']
# cookies = r.cookies['jwt-cookie']
# print 'token:', token
# print 'jwt-cookie:', cookies

rr = requests.post(url, data={'email': '554357654@qq.com', 'username': 'aegis'})
# rr = requests.get('http://127.0.0.1:8000/api-auth/users')
print rr.content



# regex_str = '\[(\d\d/[a-zA-Z]{3}/\d{4}:\d\d:\d\d).*?\].*?GET\s+(.*?)\?.*"(\d+\.\d+)"$'
# regex = re.compile(r'%s' % regex_str, re.S)
#
# s = '139.199.99.155 - - [22/Sep/2017:10:06:27 +0800] "GET /fico/score?accounts=990004&mobile=' \
#     '478743689a65fceeee803e1eae6b49c9&orderId=429142911010&sign=5cbcfa568619da9dd1eca04c68e1f6dd ' \
#     'HTTP/1.1" 200 243 "-" "Apache-HttpClient/4.5.3 (Java/1.7.0_71)" "-" "0.011"139.199.99.155 - - ' \
#     '[22/Sep/2017:10:06:27 +0800] "GET /fico/score?accounts=990004&mobile=478743689a65fceeee803e1eae6b49c9&' \
#     'orderId=429142911010&sign=5cbcfa568619da9dd1eca04c68e1f6dd HTTP/1.1" 200 243 "-" ' \
#     '"Apache-HttpClient/4.5.3 (Java/1.7.0_71)" "-" "0.011"'
#
# print regex.findall(s)
