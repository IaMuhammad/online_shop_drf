from rest_framework import serializers

from apps.models import User


class UserDetailModelSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'region', 'district')

    def get_region(self, obj: User):
        if obj.district:
            return {
                'id': obj.district.region.id,
                'name': obj.district.region.name,
            }
        return {
            'id': 1,
            'name': 'Andijon'
        }

    def get_district(self, obj: User):
        if obj.district:
            return {
                'id': obj.district.id,
                'name': obj.district.name,
            }
        return {
            'id': 1,
            'name': 'Andijon'
        }
