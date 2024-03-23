from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import User
from apps.serializers.users.change_number import UserChangeNumberModelSerializer
from apps.serializers.users.change_password import UserChangePasswordModelSerializer


class UserChangePhoneNumberAPIVIew(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangeNumberModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['user'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['user'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
