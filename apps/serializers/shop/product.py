from rest_framework import serializers

from apps.models import Banner


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'name', 'image')
