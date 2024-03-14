from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Flow
from apps.serializers.shop.flow import FlowListSerializer, FlowCreateSerializer


class FlowListAPIView(ListAPIView):
    queryset = Flow.objects.filter(is_active=True)
    serializer_class = FlowListSerializer

    @swagger_auto_schema(tags=['shop'])

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FlowCreateAPIView(CreateAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['shop'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
