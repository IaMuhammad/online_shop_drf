from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Request
from apps.serializers.shop.request import RequestListModelSerializer


class RequestListAPIView(ListAPIView):
    serializer_class = RequestListModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RequestCreateAPIView(CreateAPIView):
    serializer_class = RequestListModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.all()

    @swagger_auto_schema(tags=['shop'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
