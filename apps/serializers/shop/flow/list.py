from rest_framework import serializers

from apps.models import Flow


class FlowListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Flow
        fields = ('id', 'name', 'product',)

    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'description': obj.product.description,
            'get_image': self.context.get('request')._current_scheme_host + obj.product.get_image.image.url
        }
