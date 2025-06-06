from django.contrib.auth import authenticate
from django.db import models
from django.db.models import F
from django.db.models.functions import Concat, Cast
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.models import User


class UserUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'district')
