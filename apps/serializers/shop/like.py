from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.models import Product, Like


class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'is_discount', 'discount_price')


class LikeModelSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('id', 'product_id')

    def validate_product_id(self, value):
        if product := Product.objects.filter(id=value).first():
            return product
        raise serializers.ValidationError(_('Product does not exist'))
