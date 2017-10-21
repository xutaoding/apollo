from rest_framework import serializers

from models import MiddleFileModel


class HtmlFileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleFileModel
        fields = ['crt', 'username', 'url', 'fn_md5', 'ext']


