from rest_framework import serializers

from apps.models import User


class BalanceSerializer(serializers.ModelSerializer):
    paid = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'balance', 'paid')

    @staticmethod
    def get_paid(obj: User):
        return obj.all_balance - obj.balance
