from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Order
from apps.serializers.shop.order import OrderCreateModelSerializer, OrderListModelSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['shop'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user)
        return Order.objects.none()
