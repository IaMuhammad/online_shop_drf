from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.serializers.users import SignUPModelSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = SignUPModelSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=['user'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
