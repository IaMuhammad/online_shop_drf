from rest_framework import serializers

from apps.models import Flow


class FlowDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ('id',)
