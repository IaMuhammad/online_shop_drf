from rest_framework import serializers

from apps.models import Flow


class FlowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ('id', 'name', 'product')

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = self.context.get('request').user
        return data
