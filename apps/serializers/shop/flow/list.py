from rest_framework import serializers

from apps.models import Flow
from root.settings import DOMAIN


class FlowListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Flow
        fields = ('id', 'name', 'product', 'url')

    def get_product(self, obj: Flow):
        if obj.product.get_image:
            image = obj.product.get_image.image.url
        else:
            image = ''
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'description': obj.product.description,
            'pay': obj.product.pay,
            'get_image': image,
        }

    def get_url(self, obj):
        return f'/shop/flow/{obj.id}'
