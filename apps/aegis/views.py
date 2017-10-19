# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from ..base_view import BaseAPIView
from .models import AegisFileModel
from .serializers import HtmlFileModelSerializer

from lib.utils import gen_md5, download_html


# Create your views here.
class FileAPIView(BaseAPIView, generics.CreateAPIView):
    model_class = AegisFileModel
    queryset = model_class.objects.all()
    serializer_class = HtmlFileModelSerializer

    def post(self, request, *args, **kwargs):
        print request
        url = self.value_from_request(key='url', to_join=True)
        download_html(url)

        request.data._mutable = True
        request.data['fn_md5'] = gen_md5(url)
        request.data._mutable = False

        return self.create(request, *args, **kwargs)




