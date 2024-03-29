from rest_framework import serializers

from apps.models import Flow, Product


class FlowDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Flow
        fields = ('id', 'name', 'product',)

    def get_product(self, obj: Flow):
        if obj.product.get_image:
            image = obj.product.get_image.image.url
        else:
            image = ''
        user = self.context.get('request').user

        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'description': obj.product.description,
            'delivery': obj.product.delivery,
            'price': obj.product.price,
            'is_discount': obj.product.is_discount,
            'discount_price': obj.product.discount_price,
            'order_count': obj.product.get_order_count,
            'color': obj.product.get_color,
            'size': obj.product.get_size,
            'is_liked': obj.product.is_liked(user),
            'images': self.get_images(obj.product),  #
            'get_image': image
        }

    @staticmethod
    def get_images(obj: Product):
        images = []
        for image in obj.get_images:
            images.append(image.image.url)
        return images
