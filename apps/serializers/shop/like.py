from rest_framework import serializers

from apps.models import Product


class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'is_discount', 'discount_price')
