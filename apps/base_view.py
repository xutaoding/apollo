# -*- coding: utf-8 -*-

import json
import uuid
import types
from copy import deepcopy

from django.core.exceptions import FieldError
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from lib.crypto import AESCipher


class BaseAPIView(object):
    model_class = None

    # def check_permissions(self, request):
    #     model = get_user_model()
    #
    #     try:
    #         model.objects.get(username='admin')
    #     except(
    #             FieldError,
    #             model.DoesNotExist,
    #             model.MultipleObjectsReturned
    #     ) as exc:
    #         msg = 'Permission error: {}, Msg: require administrator to handle!'
    #         raise NotAuthenticated(msg.format(str(exc)))

    def value_from_request(self, key, default=None, request=None, to_join=False, delimiter=''):
        """ 获取 request POST 方法的data数据:
            self.request is request (self.request == request) and
            self.request.data is request.data (self.request.data == request.data) and
            self.request.data is request.POST (self.request.data == request.POST)

            (1): request.POST (type: `django.http.request.QueryDict`)
            (2): request.data (type: `django.http.request.QueryDict`)
            (3): self.request.data (type:`rest_framework.request.Request`)
        """

        request = request or self.request
        data = dict(request.data or request.GET)
        variable_types = (types.ListType, types.TupleType)

        if not to_join and isinstance(data.get(key, default), variable_types):
            return delimiter.join(data.get(key, default))

        return data.get(key, default)

    def get_or_none(self, *args, **kwargs):
        obj = None
        model_class = kwargs.pop('model_class', None) or self.model_class

        try:
            obj = model_class.objects.get(*args, **kwargs)
        except model_class.DoesNotExist:
            pass

        return obj

    def get_or_create_once(self, *args, **kwargs):
        for_write = kwargs.pop('for_write', {})
        model_class = kwargs.pop('model_class', None) or self.model_class

        try:
            obj = model_class.objects.get(*args, **kwargs)
        except (model_class.DoesNotExist, ):
            obj = model_class.objects.create(**for_write)

        return obj

    def decrypt_from_request(self, request=None):
        request = request or self.request
        print request.data
        print request.data['en_token']
        encrypt_msg = request.data.pop('en_token')

        try:
            decrypt_msg = AESCipher(encrypt_msg).decrypt()
        except ValueError:
            return Response({'message': 'Encrypt data is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        data = json.loads(decrypt_msg)

        for key, value in data.iteritems():
            request.data[key] = value

    @property
    def uuid(self):
        return str(uuid.uuid4()).replace('-', '')

    @property
    def status_ok(self):
        return [getattr(status, attr) for attr in dir(status) if attr.startswith('HTTP_20')]

    def get_user_data(self, request=None):
        request = request or self.request

        assert 'email' in request.data, "`email` required"
        assert 'username' in request.data, "`username` required"

        data = deepcopy(request.data)
        user_fields = ['username', 'password', 'email', 'is_superuser']
        user_data = {field: data.get(field, False) for field in user_fields}
        user_data.update(is_staff=True, is_active=True)

        return user_data

    @property
    def default_response(self):
        return {'isSuccess': False, 'message': ''}



