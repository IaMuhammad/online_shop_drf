from django.contrib.auth import authenticate
from django.db import models
from django.db.models import F
from django.db.models.functions import Concat, Cast
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.models import User
from apps.models.user import Region, District


class RegionSelectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictSelectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')
