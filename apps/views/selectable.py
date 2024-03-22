from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from apps.models.user import Region, District
from apps.serializers.selectable import RegionSelectModelSerializer, DistrictSelectModelSerializer


class RegionSelectListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSelectModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('name',)
    pagination_class = None

    @swagger_auto_schema(tags=['selectable'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DistrictSelectListAPIView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSelectModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('region',)
    search_fields = ('name',)
    pagination_class = None

    @swagger_auto_schema(tags=['selectable'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

