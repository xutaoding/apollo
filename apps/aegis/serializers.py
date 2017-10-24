from rest_framework import serializers

from models import (
    MiddleFileModel, WalletModel
)


class MiddleFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleFileModel
        fields = ['crt', 'spider_task_id', 'username', 'url', 'filename', 'ext', 'file_utility']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletModel
        fields = ['crt', 'username']


