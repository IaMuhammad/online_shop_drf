from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.serializers.users import SignInSerializer, SendMessageSerializer


class SignInGenericAPIView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=['user'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = _('Muvaffaqiyatli!')
        return Response({'response': message,
                         'data': serializer.data},
                        status=HTTP_200_OK)


class ConfirmSMSCodeGenericAPIView(GenericAPIView):
    serializer_class = SendMessageSerializer

    @swagger_auto_schema(tags=['user'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = _('We sent confirmation code to your phone number!')
        return Response({'response': message}, status=HTTP_200_OK)
