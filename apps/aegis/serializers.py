from rest_framework import serializers

from models import (
    MiddleFileModel, WalletModel,
    SpiderTasksModel
)


class MiddleFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleFileModel
        fields = ['crt', 'spider_task_id', 'username', 'url', 'filename', 'ext', 'file_utility']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletModel
        fields = ['crt', 'username']


class SpiderTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiderTasksModel
        fields = [field.name for field in model._meta.fields if field.name != 'id']
        # fields = [
        #     'crt', 'username', 'spider_task_id', 'spider_description', 'robotstxt_obey',
        #     'cookies_enabled', 'download_delay', 'concurrent_requests', 'other_configure',
        #     'request_method', 'request_cookies', 'request_headers', 'proxy_ip_enabled',
        #     'login_username', 'login_password'
        # ]


