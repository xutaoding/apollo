# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import views

urlpatterns = [
    url(r'upload$', views.UploadAPIView.as_view(), name='aegis_upload'),
    url(r'(?P<username>.*?)/payment$', views.IsPaymentUser.as_view(), name='aegis_payment'),
    url(r'spider-task/(?P<action>.*?)$', views.SpiderTasksAPIView.as_view(), name='aegis_spider_task'),
]


