from rest_framework import serializers

from apps.models import Request


class RequestCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'card', 'money')

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = self.context['request'].user
        return data


class RequestListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'user', 'card', 'money', 'status', 'date')
