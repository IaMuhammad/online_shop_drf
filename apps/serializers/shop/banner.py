from rest_framework import serializers

from apps.models import Banner


class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'name', 'image')
