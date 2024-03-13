from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Category

class CategoryListAPIView(APIView):

    @swagger_auto_schema(tags=['shop'])
    def get(self, request, *args, **kwargs):
        qs = Category.objects.all()
        return Response(qs)
