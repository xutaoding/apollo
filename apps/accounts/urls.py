# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import views

router = routers.DefaultRouter()
router.register(r'accounts', views.UserViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include('rest_framework.urls', namespace='rest_framework')),

    url(r'token/obtain$', obtain_jwt_token),
    url(r'token/refresh$', refresh_jwt_token),

    url(r'login$', views.UserLoginAPIView.as_view(), name='user_login'),
    url(r'mail/send$', views.SenderMailCodeAPIView.as_view(), name='sender_mail'),
    url(r'register$', views.RegisterUserAPIView.as_view(), name='register_user'),
    url(r'forget-password$', views.ForgetPasswordAPIView.as_view(), name='register_user'),
]


