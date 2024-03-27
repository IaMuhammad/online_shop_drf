from rest_framework import serializers

from apps.models import Product, Like


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
        'id', 'name', 'description', 'price', 'is_discount', 'discount_price', 'category', 'is_liked', 'image')

    def get_is_liked(self, obj: Product):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.is_liked(user)
        return False

    @staticmethod
    def get_image(obj: Product):
        return obj.get_image.image.url

    def get_category(self, obj: Product):
        return {
            'id': obj.category.id,
            'name': obj.category.name,
        }


class ProductDetailSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'delivery', 'price', 'is_discount', 'discount_price', 'order_count', 'color',
            'size', 'is_liked', 'images'
        )

    def get_order_count(self, obj: Product):
        return 0

    def get_is_liked(self, obj: Product):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.is_liked(user)
        return False

    def get_images(self, obj: Product):
        images = []
        for image in obj.get_images:
            images.append(image.image.url)
        return images

    @staticmethod
    def get_color(obj: Product):
        return obj.get_color

    @staticmethod
    def get_size(obj: Product):
        return obj.get_size
