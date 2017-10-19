from rest_framework import serializers

from models import AegisFileModel


class HtmlFileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AegisFileModel
        fields = ['crt', 'username', 'url', 'fn_md5', 'ext']


