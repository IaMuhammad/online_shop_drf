from rest_framework import serializers

from apps.models import Flow


class FlowStatisticsSerializer(serializers.ModelSerializer):
    new_count = serializers.SerializerMethodField()
    accepted_count = serializers.SerializerMethodField()
    delivering_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()
    recall_count = serializers.SerializerMethodField()
    spam_count = serializers.SerializerMethodField()
    canceled_count = serializers.SerializerMethodField()
    hold_count = serializers.SerializerMethodField()
    archived_count = serializers.SerializerMethodField()

    class Meta:
        model = Flow
        fields = (
            'id', 'name', 'new_count', 'accepted_count', 'delivering_count', 'completed_count', 'recall_count',
            'spam_count', 'canceled_count', 'hold_count', 'archived_count',
        )

    @staticmethod
    def get_new_count(obj: Flow):
        return obj.get_new

    @staticmethod
    def get_accepted_count(obj: Flow):
        return obj.get_accepted

    @staticmethod
    def get_delivering_count(obj: Flow):
        return obj.get_delivering

    @staticmethod
    def get_completed_count(obj: Flow):
        return obj.get_completed

    @staticmethod
    def get_recall_count(obj: Flow):
        return obj.get_recall

    @staticmethod
    def get_spam_count(obj: Flow):
        return obj.get_spam

    @staticmethod
    def get_canceled_count(obj: Flow):
        return obj.get_canceled

    @staticmethod
    def get_hold_count(obj: Flow):
        return obj.get_hold

    @staticmethod
    def get_archived_count(obj: Flow):
        return obj.get_archived
