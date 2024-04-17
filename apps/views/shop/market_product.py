from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from apps.models import Product
from apps.serializers.shop.market_product import MarketProductListSerializer


class MarketProductListAPIView(ListAPIView):
    serializer_class = MarketProductListSerializer
    queryset = Product.objects.filter(add_flow=True).order_by('id')
    filter_backends = [SearchFilter]
    search_fields = ('name',)

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
