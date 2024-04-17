from django.utils.translation.trans_null import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import User
from apps.serializers.users.send_message import UserChangeNumberSerializer
from apps.utils.send_message import send_message_phone


class SendMessageAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserChangeNumberSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['user'], request_body=UserChangeNumberSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserChangeNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_message_phone(serializer.validated_data.get('phone_number'))
        return Response(data={'success': _('We sent message')})
