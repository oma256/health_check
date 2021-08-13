from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from fcm_django.models import FCMDevice

from apps.commons.constants.helpers import disable_for_loaddata
from apps.commons.constants.notification import (
    NOTIFICATION_TYPE, INDICATOR,
    NOTIFICATION_TITLES_LN,
    NOTIFICATION_MESSAGE_LN
)
from apps.users.models import User, Patient


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='notifications',
        on_delete=models.CASCADE
    )
    notification_type = models.CharField(
        verbose_name='Тип',
        choices=NOTIFICATION_TYPE,
        max_length=12
    )
    is_viewed = models.BooleanField(verbose_name='Просмотрено?', default=False)
    deviation_count = models.PositiveSmallIntegerField(
        verbose_name='Кол-во отклонений',
        default=0,
    )
    create_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
        null=True,
    )

    class Meta:
        ordering = ['-create_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.user.get_full_name

    def send_fcm(self):
        FCMDevice.objects.filter(user=self.user).send_message(
            data=dict(
                id=self.id,
                title=self._get_title(),
                body=self._get_body(),
                click_action=self.notification_type,
            ),
            api_key=settings.FCM_DJANGO_SETTINGS.get('FCM_SERVER_KEY', None)
        )

    def _get_title(self):
        return NOTIFICATION_TITLES_LN.get(self.user.language)

    def _get_body(self):
        return NOTIFICATION_MESSAGE_LN.get(self.notification_type)\
            .get(self.user.language).format(**self.message_variables)

    @property
    def message_variables(self):
        return dict(
            deviation_count=self.deviation_count
        )

    @classmethod
    def create_indicator_type(cls, queryset=None):
        query = queryset or Patient.objects.all()

        _patients = query.exclude(
            indicator__create_at__date=timezone.now().today()
        ).filter(user__is_active=True)

        for patient in _patients:
            cls.objects.create(user=patient.user, notification_type=INDICATOR)

    @classmethod
    def get_notifications_today(cls, user):
        return cls.objects.filter(
            create_at__date=timezone.now().today(),
            user=user,
        ).order_by('notification_type', '-create_at').distinct('notification_type')


@receiver(post_save, sender=Notification)
@disable_for_loaddata
def post_save_notice(sender, instance, created, **kwargs):
    if created:
        instance.send_fcm()
