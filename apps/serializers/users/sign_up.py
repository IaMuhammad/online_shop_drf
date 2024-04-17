from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models import F
from django.db.models.functions import Concat, Cast
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.models import User


class SignUPModelSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password', '12345678'))
        return super().create(validated_data)

