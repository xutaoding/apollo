# -*- coding: utf-8 -*-

import json
from rest_framework import status
from rest_framework.response import Response

from .crypto import AESCipher


def decrypt_request(method):
    decrypt_methods = ['POST', 'PUT', 'DELETE']

    def wrapper(self, request=None, *args, **kwargs):
        request = request or self.request

        if request.method not in decrypt_methods or 'login' in request.path:
            return method(self, request, *args, **kwargs)

        print 'request before:'
        print request.data
        print type(request.data)
        request.data['username'] = request.user.username

        try:
            encrypt_data = request.data.pop('en_token')
            decrypt_data = AESCipher(encrypt_data).decrypt()
        except (ValueError, KeyError) as e:
            return Response(
                data={'message': 'Encrypt data is invalid: {}'.format(str(e))},
                status=status.HTTP_404_NOT_FOUND
            )

        for key, value in json.loads(decrypt_data).iteritems():
            request.data[key] = value

        return method(self, request, *args, **kwargs)

    return wrapper


