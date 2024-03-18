from rest_framework import serializers

from apps.models import Product


class MarketProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'pay')
