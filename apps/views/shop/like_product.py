from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.filters import LikeFilter
from apps.models import Product, Like
from apps.serializers.shop.like import LikeListSerializer, LikeModelSerializer


class LikeProductListAPIView(ListAPIView):
    serializer_class = LikeListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_class = LikeFilter

    def get_queryset(self):
        return Product.objects.filter(like__user=self.request.user)

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LikeProductCreateAPIView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['shop'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        like, _ = Like.objects.get_or_create(user=request.user)
        product = serializer.validated_data.get('product_id')
        if like.products.filter(id=product.pk).first():
            like.products.remove(product)
            return Response(data={'status': 'Like removed'})
        else:
            like.products.add(product)
            return Response(data={'status': 'Liked'})
