from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Banner
from apps.serializers.shop.banner import BannerListSerializer


class BannerListAPIView(APIView):
    serializer_class = BannerListSerializer

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.filter(is_active=True)
        serializer = self.serializer_class(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
