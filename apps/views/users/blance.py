from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.models import User
from apps.serializers.users import BalanceSerializer


class BalanceRetrieveAPIView(RetrieveAPIView):
    serializer_class = BalanceSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=['user'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
