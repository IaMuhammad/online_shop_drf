from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Flow
from apps.serializers.shop.flow import FlowListSerializer


class FlowListAPIView(ListAPIView):
    queryset = Flow.objects.filter(is_active=True)
    serializer_class = FlowListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
