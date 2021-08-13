from django.utils import timezone
from rest_framework import serializers

from apps.indicators.models import PatientIndicator


class PatientIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientIndicator
        fields = [
            'id',
            'patient',
            'dyspnea',
            'position_bed',
            'heartbeat',
            'stack',
            'weight',
            'arterial_pressure',
            'pulse',
            'create_at',
            'deviation_count'
        ]
        extra_kwargs = {
            'patient': {
                'read_only': True
            },
            'create_at': {
                'read_only': True
            },
            'deviation_count': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        patient = self.context['request'].user.patient
        if patient.indicator.filter(create_at__contains=timezone.now().date()).exists():
            raise serializers.ValidationError({"message": "Вы уже заполнили анкету на сегодня."})

        return super().create(validated_data)

    def save(self, **kwargs):
        self.validated_data['patient'] = self.context['request'].user.patient
        return super().save(**kwargs)


class PatientIndicatorDetailSerializer(serializers.ModelSerializer):
    dyspnea = serializers.DictField(source='dyspnea_check')
    position_bed = serializers.DictField(source='position_bed_check')
    heartbeat = serializers.DictField(source='heartbeat_check')
    stack = serializers.DictField(source='stack_check')
    weight = serializers.DictField(source='weight_check')
    arterial_pressure = serializers.DictField(source='arterial_pressure_check')
    pulse = serializers.DictField(source='pulse_check')

    class Meta:
        model = PatientIndicator
        fields = [
            'id',
            'patient',
            'create_at',
            'dyspnea',
            'position_bed',
            'heartbeat',
            'stack',
            'weight',
            'arterial_pressure',
            'pulse',
            'deviation_count'
        ]


class DoctorPatientIndicatorHistory(serializers.ModelSerializer):
    class Meta:
        model = PatientIndicator
        fields = [
            'id',
            'patient',
            'dyspnea',
            'position_bed',
            'heartbeat',
            'stack',
            'weight',
            'arterial_pressure',
            'pulse',
            'create_at',
            'deviation_count'
        ]
        extra_kwargs = {
            'patient': {
                'read_only': True
            },
            'create_at': {
                'read_only': True
            },
            'deviation_count': {
                'read_only': True
            }
        }
