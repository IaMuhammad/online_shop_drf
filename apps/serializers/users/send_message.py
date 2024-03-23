from django.contrib.auth.hashers import check_password, make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.models import User


class UserChangeNumberModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'code')
