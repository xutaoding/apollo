# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from lib.decorator import decrypt_request
from lib.utils import gen_md5
from .models import (
    MiddleFileModel, WalletModel,
    SpiderTasksModel,
)
from .serializers import (
    MiddleFileSerializer, WalletSerializer,
    SpiderTaskSerializer
)
from ..base_view import BaseAPIView


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
        """ 上传(参数)文件 """
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
    serializer_class = SpiderTaskSerializer

    file_model_class = MiddleFileModel
    file_serializer_class = MiddleFileSerializer

    def create_file_record(self, request=None):
        """ 多用户同时爬虫时下载网页需要Celery """
        request = request or self.request
        fields = [field.name for field in self.file_model_class._meta.fields
                  if field.name not in ['crt', 'id']]

        data = {key: request.data[key] for key in fields if request.data.get(key)}
        data.update(filename=gen_md5(data['url']))

        s = self.file_serializer_class(data=data)
        if s.is_valid():
            s.save()

            save_path = settings.FILE_PATH + s.data['filename'] + s.data['ext']
            download_request.delay(s.data['url'], save_path)

            return Response(data=s.data, status=status.HTTP_201_CREATED)

        return Response(data={'message': u'该网址的爬虫已存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @decrypt_request
    def get(self, request, *args, **kwargs):
        pass

    @decrypt_request
    def post(self, request, *args, **kwargs):
        """ 创建爬虫时下载网页(celery) """

        assert kwargs.pop('action', None) == 'create', ' Request post method to create spider task'

        request.data['spider_task_id'] = self.uuid
        response = self.create_file_record(request)
        if response.status_code not in self.status_ok:
            return response

        return self.create(request, *args, **kwargs)

    @decrypt_request
    def put(self, request, *args, **kwargs):
        pass

    @decrypt_request
    def delete(self, request, *args, **kwargs):
        pass






