# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from ..base_view import BaseAPIView
from .models import AegisFileModel
from .serializers import HtmlFileModelSerializer

from lib.utils import gen_md5, download_html


# Create your views here.
class IsPaymentUser(BaseAPIView, generics.RetrieveAPIView):
    model_class = None
    queryset = None
    serializer_class = None



class DownloaderAPIView(BaseAPIView, generics.CreateAPIView):
    model_class = AegisFileModel
    queryset = model_class.objects.all()
    serializer_class = HtmlFileModelSerializer

    def post(self, request, *args, **kwargs):
        decrypted_data = self.decrypt_from_request(request)
        if decrypted_data:
            return decrypted_data

        url = self.value_from_request(key='url', request=request)
        name = self.value_from_request(key='url', request=request)
        desc = self.value_from_request(key='description', request=request)
        download_html(url)

        request.data['fn_md5'] = gen_md5(url)

        return self.create(request, *args, **kwargs)




