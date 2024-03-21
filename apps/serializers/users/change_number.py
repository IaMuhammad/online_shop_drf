from django.contrib.auth.hashers import check_password, make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.models import User


class UserChangeNumberModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number')

    def validate_check_password(self, value):
        if check_password(value, self.instance.password):
            return value
        raise serializers.ValidationError(_('Entered wrong password'))

    def validate_code(self, value):
        if value != '0000':
            raise serializers.ValidationError(_('Entered wrong code!'))
        return value
