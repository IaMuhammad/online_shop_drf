from django.contrib.auth.hashers import check_password, make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.models import User


class UserChangePasswordModelSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('id', 'check_password', 'password')

    def validate_check_password(self, value):
        if check_password(value, self.instance.password):
            return value
        raise serializers.ValidationError(_('Entered wrong password'))

    def validate_password(self, value):
        return make_password(value)
