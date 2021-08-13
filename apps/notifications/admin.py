from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'get_user',
        'notification_type',
        'deviation_count',
        'is_viewed',
        'create_at',
    ]

    list_filter = ['notification_type']

    def get_user(self, obj):
        return obj.user.get_full_name

    get_user.short_description = 'пациент (Ф.И.О)'
