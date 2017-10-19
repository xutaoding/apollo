# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import serializers, viewsets, generics

from ..base_view import BaseAPIView
from .permissions import IsOwnerOrReadOnly
from .models import MailVerifyCode
from .serializers import MailVerifyCodeSerializer, UserSerializer
from lib.mail import get_validation_code
from elastic_jobs.tasks_pkg.mail.tasks import send_mail_by_celery


# Create your views here.
# Deprecated: Serializers define the API representation.
class PreUserSerializer(serializers.HyperlinkedModelSerializer):
    """ Test to deprecated """
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# Deprecated: ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """ Test to deprecated """
    queryset = User.objects.all()
    serializer_class = PreUserSerializer


# Deprecated: discard user register.
class UserRegisterDeprecatedView(BaseAPIView, generics.CreateAPIView):
    """ The Class that to register user was deprecated """

    model_class = User
    serializer_class = User  # User Serializer should error.
    queryset = User.objects.all()

    @property
    def data_from_request(self):
        print '33:', id(self.request)
        print 'request data:', self.request.data
        return {k: ''.join(v) for k, v in self.request.data.items()}

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create_user(**self.data_from_request)
            user.save()
        except Exception as exc:
            return Response(
                data={'isSuccess': False, 'message': str(exc)},
                status=500
            )

        return Response({'isSuccess': True, 'message': 'Register user success!'})


class UserLoginAPIView(BaseAPIView, ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        result = self.decrypt_from_request(request=request)
        if result: return result

        return super(ObtainJSONWebToken, self).post(request, *args, **kwargs)


class SenderMailCodeAPIView(BaseAPIView, generics.GenericAPIView):
    model_class = MailVerifyCode
    serializer_class = MailVerifyCodeSerializer
    queryset = model_class.objects.all()

    permission_classes = ()

    def send_mail_and_save(self, username, verify_code, recipient_list):
        data = self.default_response
        subject = u'宙斯盾-用户注册校验码邮件'
        message = u'Hi {},\n\t您的注册确认码为: {}\n\t' \
                  u'提示：10分钟内有效，请及时注册\n\n\t欢迎使用宙斯盾平台系统。'

        mvc = self.model_class.objects.filter(owner_name=username).first()
        if mvc and (mvc.crt + timedelta(minutes=10)) >= timezone.now():
            data.update(message=u'邮箱验证码10分钟内均有效')
            return Response(data=data, status=status.HTTP_201_CREATED)

        send_mail_by_celery.delay(subject, message.format(username, verify_code), recipient_list)

        s = self.serializer_class(data={'verify_code': verify_code, 'owner_name': username})
        if s.is_valid():
            s.save()
            data.update(isSuccess=True, message='验证码已发送到你的邮箱')
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(s.errors, status=status.HTTP_404_NOT_FOUND)

    def send_by_register(self, request):
        data = self.default_response

        # Decrypt data from request
        username = self.value_from_request(key='username', request=request)
        recipient = self.value_from_request(key='email', request=request)
        recipient_list = list(recipient) if isinstance(recipient, (list, tuple)) else [recipient]

        # User validation
        if User.objects.filter(username=username).count() > 0:
            data.update(message=u'该用户名已被注册')
            return Response(data=data, status=status.HTTP_201_CREATED)

        if User.objects.filter(email=recipient).count() >= 1:
            data.update(message=u'该邮箱已被注册')
            return Response(data=data, status=status.HTTP_201_CREATED)

        User.objects.create(**self.get_user_data_from_aegis())
        verify_code = get_validation_code()

        return self.send_mail_and_save(username, verify_code, recipient_list)

    def send_by_forgetter(self, request):
        data = self.default_response
        verify_code = get_validation_code()
        username = self.value_from_request(key='username', request=request)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            data.update(message=u'用户名不正确')
            return Response(data=data, status=status.HTTP_202_ACCEPTED)

        return self.send_mail_and_save(username, verify_code, [user.email])

    def post(self, request, *args, **kwargs):
        """ Sending mail should administrator permission """

        # Decrypt data from request
        result = self.decrypt_from_request(request)
        if result is not None:
            return result

        if request.data.get('forgetter', False) is False:
            return self.send_by_register(result)

        return self.send_by_forgetter(result)


class RegisterUserAPIView(BaseAPIView, generics.CreateAPIView):
    model_class = MailVerifyCode
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )

    def post(self, request, *args, **kwargs):
        data = self.default_response
        result = self.decrypt_from_request(request)
        if result: return result

        print request.data

        username = self.value_from_request(key='username', request=request)
        password = self.value_from_request(key='password', request=request)
        verify_code = self.value_from_request(key='verify_code', request=request)
        mvc = self.model_class.objects.filter(owner_name=username).first()

        if mvc is None:
            data['message'] = u'请发送邮箱验证码'
            return Response(data=data, status=status.HTTP_200_OK)

        if (mvc.crt + timedelta(minutes=10)) < timezone.now():
            data['message'] = u'您的邮箱验证码已过期'
            return Response(data=data, status=status.HTTP_200_OK)

        if mvc.verify_code != verify_code:
            data['message'] = u'邮箱验证码错误'
            return Response(data=data, status=status.HTTP_200_OK)

        user = User.objects.get(username=username)
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save()

        data.update(isSuccess=True, message='OK')
        return Response(data=data, status=status.HTTP_200_OK)


class ForgetPasswordAPIView(BaseAPIView, generics.CreateAPIView):
    model_class = User
    # serializer_class = UserSerializer
    # queryset = model_class.objects.all()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """ 已经注册该用户 """

        data = self.default_response
        result = self.decrypt_from_request(request)
        if result: return result

        username = self.value_from_request(key='username', request=request)
        password = self.value_from_request(key='password', request=request)
        verify_code = self.value_from_request(key='verify_code', request=request)

        if verify_code is None:
            data['message'] = u'请发送邮箱验证码'
            return Response(data=data, status=status.HTTP_201_CREATED)

        mvc = MailVerifyCode.objects.filter(owner_name=username).first()
        if not mvc or (mvc.crt + timedelta(minutes=10)) < timezone.now():
            data['message'] = u'请发送邮箱验证码,可能已过期'
            return Response(data=data, status=status.HTTP_201_CREATED)

        if mvc.verify_code != verify_code:
            data.update(message=u'验证码不正确')
            return Response(data=data, status=status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

        data.update(isSuccess=True, message='OK')
        return Response(data=data, status=status.HTTP_200_OK)
