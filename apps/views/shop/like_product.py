from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Product
from apps.serializers.shop.like import LikeListSerializer
from apps.serializers.shop.product import ProductListSerializer


class LikeProductListAPIView(ListAPIView):
    serializer_class = LikeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(like__user=self.request.user)

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
