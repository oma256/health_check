from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='notification_type')

    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'deviation_count',
            'is_viewed',
            'create_at',
        ]
