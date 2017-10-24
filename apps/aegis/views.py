# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from ..base_view import BaseAPIView
from .models import (
    MiddleFileModel, WalletModel,
    SpiderTasksModel,
)
from .serializers import (
    MiddleFileSerializer, WalletSerializer,
)

from lib.utils import gen_md5, download_html
from lib.decorator import decrypt_request


# Create your views here.
class IsPaymentUser(BaseAPIView, generics.RetrieveAPIView):
    model_class = WalletModel
    lookup_field = 'username'
    serializer_class = WalletSerializer
    # permission_classes = ()

    def get(self, request, *args, **kwargs):
        instance = self.model_class.objects.filter(username=request.user.username).last()
        serializer = self.get_serializer(instance)
        data = serializer.data
        is_payment = data.get(self.lookup_field) == request.user.username
        data.update(is_payment=is_payment)

        return Response(data=data)


class UploadAPIView(BaseAPIView, generics.ListCreateAPIView):
    model_class = MiddleFileModel
    queryset = model_class.objects.all()
    serializer_class = MiddleFileSerializer

    def post(self, request, *args, **kwargs):
        decrypted_data = self.decrypt_from_request(request)
        if decrypted_data:
            return decrypted_data

        request.data['username'] = request.user.username
        url = self.value_from_request(key='url', request=request)
        request.data['filename'] = gen_md5(url)

        download_html(url)

        return self.create(request, *args, **kwargs)


class SpiderTasksAPIView(BaseAPIView,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.ListCreateAPIView):
    model_class = SpiderTasksModel
    queryset = model_class.objects.all()
    serializer_class = None

    @decrypt_request
    def post(self, request, *args, **kwargs):
        spider_task_id = self.uuid
        url = request.data.pop('url')
        ext = request.data.pop('ext')
        file_data = dict(
            url=url, ext=ext, filename=gen_md5(url),
            spider_task_id=spider_task_id, username=request.data['username'],
        )

        if ext is not None:
            file_data.update(file_utility='PM')

        print 'request after:'
        print request.data
        print type(request.data)

    @decrypt_request
    def put(self, request, *args, **kwargs):
        pass

    @decrypt_request
    def delete(self, request, *args, **kwargs):
        pass






