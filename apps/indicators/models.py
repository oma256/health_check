from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.commons.constants.helpers import disable_for_loaddata
from apps.commons.constants.indicator import (
    DYSPNEA_CHOICE, POSITION_BED_CHOICES, HEARTBEAT_CHOICES, STACK_CHOICES,
)
from apps.commons.constants.notification import DEVIATION
from apps.notifications.models import Notification
from apps.users.models import Patient


class PatientIndicator(models.Model):
    patient = models.ForeignKey(
        Patient,
        verbose_name='пациент',
        related_name='indicator',
        on_delete=models.CASCADE,
        null=True,
    )
    dyspnea = models.PositiveSmallIntegerField(
        verbose_name='одышка',
        choices=DYSPNEA_CHOICE
    )
    position_bed = models.PositiveSmallIntegerField(
        verbose_name='положение в постели',
        choices=POSITION_BED_CHOICES
    )
    heartbeat = models.PositiveSmallIntegerField(
        verbose_name='сердцебиение',
        choices=HEARTBEAT_CHOICES
    )
    stack = models.PositiveSmallIntegerField(
        verbose_name='отеки',
        choices=STACK_CHOICES
    )
    weight = models.PositiveSmallIntegerField(verbose_name='вес')
    arterial_pressure = models.CharField(verbose_name='АД', max_length=12)
    pulse = models.PositiveSmallIntegerField(verbose_name='пульс')
    deviation = models.PositiveIntegerField(verbose_name='отклонение', null=True)
    create_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True, null=True
    )

    class Meta:
        verbose_name = 'индикатор пациента'
        verbose_name_plural = 'индикаторы пациентов'
        ordering = ['-create_at']

    def __str__(self):
        return f'Индикатор {self.patient.__str__()}'

    @property
    def deviation_count(self):
        count = 0
        if self.dyspnea_check['deviation']:
            count += 1

        if self.position_bed_check['deviation']:
            count += 1

        if self.heartbeat_check['deviation']:
            count += 1

        if self.stack_check['deviation']:
            count += 1

        if self.weight_check['deviation']:
            count += 1

        if self.arterial_pressure_check['deviation']:
            count += 1

        if self.pulse_check['deviation']:
            count += 1
        return count

    @property
    def dyspnea_check(self):
        deviation = self.dyspnea == 3
        data = dict(
            deviation=deviation,
            value=self.get_dyspnea_display(),
            description=self.get_dyspnea_display()
        )
        return data

    @property
    def position_bed_check(self):
        deviation = self.position_bed == 3

        data = dict(
            deviation=deviation,
            value=self.get_position_bed_display(),
            description=self.get_position_bed_display()
        )

        return data

    @property
    def heartbeat_check(self):
        deviation = self.heartbeat == 3

        data = dict(
            deviation=deviation,
            value=self.get_heartbeat_display(),
            description=self.get_heartbeat_display()
        )

        return data

    @property
    def stack_check(self):
        deviation = self.stack == 4 or self.stack == 3

        data = dict(
            deviation=deviation,
            value=self.get_stack_display(),
            description=self.get_stack_display()
        )
        return data

    @property
    def weight_check(self):
        deviation = False
        if self.weight > self.patient.weight:
            deviation = True
        description = _('У вас избыточный вес на %s кг') % (self.weight - self.patient.weight) \
            if deviation else ''

        data = dict(
            deviation=deviation,
            value=self.weight,
            description=description
        )
        return data

    @property
    def arterial_pressure_check(self):
        try:
            ar_top = int(self.arterial_pressure.split('/')[0])
            ar_bottom = int(self.arterial_pressure.split('/')[1])
            deviation = False
            if ar_top > 140:
                deviation = True
            if ar_bottom < 80:
                deviation = True
        except:
            deviation = None

        data = dict(
            deviation=deviation,
            value=self.arterial_pressure,
            description=self.arterial_pressure
        )

        return data

    @property
    def pulse_check(self):
        deviation = False
        if self.pulse > 90:
            deviation = True
        if self.pulse < 60:
            deviation = True

        data = dict(
            deviation=deviation,
            value=self.pulse,
            description=self.pulse
        )

        return data


@receiver(post_save, sender=PatientIndicator)
@disable_for_loaddata
def post_save_notice(sender, instance, created, **kwargs):
    if created:
        instance.deviation = instance.deviation_count
        instance.save()

    if created and instance.deviation_count:
        Notification.objects.create(
            user=instance.patient.user,
            notification_type=DEVIATION,
            deviation_count=instance.deviation_count
        )
