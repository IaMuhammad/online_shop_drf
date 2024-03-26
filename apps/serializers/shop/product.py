from rest_framework import serializers

from apps.models import Product, Like


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'is_discount', 'discount_price', 'category')

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

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'delivery', 'price', 'is_discount', 'discount_price', 'order_count', 'color',
            'size', 'is_liked'
        )

    def get_order_count(self, obj: Product):
        return 0

    def get_is_liked(self, obj: Product):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Like.objects.filter(user=user, products__in=[obj]).exists()
        return False

    @staticmethod
    def get_color(obj: Product):
        return obj.get_color

    @staticmethod
    def get_size(obj: Product):
        return obj.get_size
