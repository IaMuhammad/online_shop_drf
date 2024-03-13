from rest_framework import serializers

from apps.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'is_discount', 'discount_price')
