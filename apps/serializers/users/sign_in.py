from django.contrib.auth import authenticate
from django.db import models
from django.db.models import F
from django.db.models.functions import Concat, Cast
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.models import User


class SignInSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True, required=False)
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number', 'tokens', 'permissions'
        )

        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_tokens(self, obj):
        user = get_object_or_404(User, phone_number=obj.get('phone_number'))
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def get_permissions(self, obj):
        user = get_object_or_404(User, phone_number=obj.get('phone_number'))
        return (User.objects.filter(id=user.id).annotate(phone_concat=Concat(
            Cast(F('groups__permissions__content_type__model'), output_field=models.CharField()),
            models.Value('.'), F('groups__permissions__codename'), output_field=models.CharField())).
                values_list('phone_concat', flat=True))

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def validate_phone_number(self, obj: str):
        obj = obj.replace(' ', '')
        if obj[0] != '+':
            raise serializers.ValidationError(_('Telefon raqam `+!` bilan boshlanishi kerak'))
        if not obj[1:].isdigit():
            raise serializers.ValidationError(_('Telefon raqam raqamlardan iborat bo\lishi kerak!'))
        return obj

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', '')
        password = attrs.get('password', '')
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise AuthenticationFailed(_('Hisob maʼlumotlari notoʻgʻri, qayta urinib koʻring'))
        if not user.is_active:
            raise AuthenticationFailed(_("Hisob o'chirilgan, administrator bilan bog'laning"))
        return {
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens(),
            'phone_number': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        }