import pytz
from django.conf import settings
from import_export import resources
from import_export.fields import Field

from apps.indicators.models import PatientIndicator
from apps.commons.constants import indicator


class PatientIndicatorResources(resources.ModelResource):
    patient = Field(column_name='Пациент (Ф.И.О)')
    dyspnea = Field(column_name='Одышка')
    position_bed = Field(column_name='Положение в постели')
    heartbeat = Field(column_name='Сердцебиение')
    stack = Field(column_name='Отеки')
    weight = Field(column_name='Вес')
    arterial_pressure = Field(column_name='АД')
    pulse = Field(column_name='Пульс')
    create_at = Field(column_name='Дата/Время')

    class Meta:
        model = PatientIndicator
        fields = (
            'patient', 'dyspnea', 'position_bed', 'heartbeat', 'stack',
            'weight', 'arterial_pressure', 'pulse', 'create_at',
        )

    @staticmethod
    def dehydrate_patient(instance):
        return instance.patient.user.get_full_name

    @staticmethod
    def dehydrate_dyspnea(instance):
        if instance.dyspnea == indicator.DYSPNEA_NOT:
            return indicator.DYSPNEA_CHOICE[0][1]
        elif instance.dyspnea == indicator.DYSPNEA_UNDER_LOAD:
            return indicator.DYSPNEA_CHOICE[1][1]
        else:
            return indicator.DYSPNEA_CHOICE[2][1]

    @staticmethod
    def dehydrate_position_bed(instance):
        if instance.position_bed == indicator.POSITION_BED_HORIZONTALLY:
            return indicator.POSITION_BED_CHOICES[0][1]
        elif instance.position_bed == indicator.POSITION_BED_TWO_PILLOW:
            return indicator.POSITION_BED_CHOICES[1][1]
        else:
            return indicator.POSITION_BED_CHOICES[2][1]

    @staticmethod
    def dehydrate_heartbeat(instance):
        if instance.heartbeat == indicator.HEARTBEAT_NOT:
            return indicator.HEARTBEAT_CHOICES[0][1]
        elif instance.heartbeat == indicator.HEARTBEAT_UNDER_LOAD:
            return indicator.HEARTBEAT_CHOICES[1][1]
        else:
            return indicator.HEARTBEAT_CHOICES[2][1]

    @staticmethod
    def dehydrate_stack(instance):
        if instance.stack == indicator.STACK_FOOT:
            return indicator.STACK_CHOICES[0][1]
        elif instance.stack == indicator.STACK_SHINS:
            return indicator.STACK_CHOICES[1][1]
        else:
            return indicator.STACK_CHOICES[2][1]

    @staticmethod
    def dehydrate_weight(instance):
        return instance.weight

    @staticmethod
    def dehydrate_arterial_pressure(instance):
        return instance.arterial_pressure

    @staticmethod
    def dehydrate_pulse(instance):
        return instance.pulse

    @staticmethod
    def dehydrate_create_at(instance):
        tz = pytz.timezone(settings.TIME_ZONE)

        return instance.create_at.astimezone(
            tz=tz
        ).strftime('%d-%m-%Y | %H:%M:%S')
