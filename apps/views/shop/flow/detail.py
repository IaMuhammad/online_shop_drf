from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Flow
from apps.serializers.shop.flow.detail import FlowDetailSerializer


class FlowRetrieveAPIView(RetrieveAPIView):
    queryset = Flow.objects.filter(is_active=True)
    serializer_class = FlowDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
