from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.serializers.users import SignInSerializer


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
