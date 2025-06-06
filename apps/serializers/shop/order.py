from django.forms import model_to_dict
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
        if data.get('product').is_discount:
            data['price'] = data['product'].discount_price
        else:
            data['price'] = data['product'].price
        return data


class OrderListModelSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'product', 'color', 'size', 'flow', 'region', 'customer_name', 'customer_number', 'customer_address',
            'quantity', 'price', 'status'
        )

    def get_product(self, obj: Order):
        image = obj.product.get_image.image.url if obj.product.get_image else ''
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'image': image,
        }

    def get_color(self, obj: Order):
        return {
            'id': obj.color.id,
            'name': obj.color.value,
            'image': obj.color.image.url
        }

    def get_size(self, obj: Order):
        return model_to_dict(obj.size, ('id', 'value',))
