from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import UpdateAPIView

from apps.models import User
from apps.serializers.users.update import UserUpdateModelSerializer


class UserUpdateAPIVIew(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateModelSerializer

    @swagger_auto_schema(tags=['user'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['user'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
