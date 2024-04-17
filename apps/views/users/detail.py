from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.models import User
from apps.serializers.users import SignInSerializer, SendMessageSerializer
from apps.serializers.users.detail import UserDetailModelSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserDetailModelSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['user'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
