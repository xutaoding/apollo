# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import views

urlpatterns = [
    url(r'file/create', views.FileAPIView.as_view(), name='aegis_file'),
    # url(r'user/register', views.RegisterUserAPIView.as_view(), name='register_user'),
]


