from django.contrib.auth.models import User
from rest_framework import serializers

from models import MailVerifyCode


class MailVerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailVerifyCode
        fields = ['verify_code', 'owner_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'email', 'is_staff', 'is_active', 'last_login', 'date_joined']



