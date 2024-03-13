from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView

from apps.models import Product
from apps.serializers.shop.product import ProductListSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
