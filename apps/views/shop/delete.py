from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Flow
from apps.serializers.shop.flow import FlowCreateSerializer
from rest_framework.response import Response

from apps.serializers.shop.flow.delete import FlowDeleteSerializer


class FlowDestroyAPIView(DestroyAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowDeleteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['shop'])
    def delete(self, request, *args, **kwargs):
        if Flow.objects.filter(id=kwargs.get('pk'), is_active=True).exists():
            Flow.objects.filter(id=kwargs.get('pk')).update(is_active=False)
            return Response()
        return Response({"detail": "Not found."}, status=404)
