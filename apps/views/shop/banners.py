from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.models import Banner
from apps.serializers.shop.banner import BannerListSerializer
from apps.serializers.users import SignInSerializer


class BannerListAPIView(ListAPIView):
    serializer_class = BannerListSerializer
    queryset = Banner.objects.filter(is_active=True)

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
