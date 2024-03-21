from rest_framework import serializers

from apps.models import Order


class OrderCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'product', 'color', 'size', 'flow', 'region', 'customer_name', 'customer_number', 'customer_address',
            'quantity'
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        data['customer'] = self.context['request'].user
        return data
