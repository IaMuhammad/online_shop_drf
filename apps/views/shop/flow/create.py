from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Flow
from apps.serializers.shop.flow import FlowCreateSerializer


class FlowCreateAPIView(CreateAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['shop'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
