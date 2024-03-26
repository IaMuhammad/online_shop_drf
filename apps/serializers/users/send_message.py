from django.contrib.auth.hashers import check_password, make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.models import User


class UserChangeNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
