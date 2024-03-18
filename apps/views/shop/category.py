from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Category
from apps.serializers.shop.category import CategoryListSerializer


class CategoryListAPIView(APIView):
    serializer_class = CategoryListSerializer

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)
