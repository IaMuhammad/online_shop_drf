from rest_framework import serializers

from apps.models import Product


class MarketProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'pay', 'image')

    def get_image(self, obj: Product):
        return obj.get_image.image.url
