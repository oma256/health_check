from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from import_export.formats import base_formats

from apps.indicators.resources import PatientIndicatorResources
from import_export.admin import ExportMixin
from apps.indicators.models import PatientIndicator


@admin.register(PatientIndicator)
class PatientIndicator(ExportMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'get_patient',
        'dyspnea',
        'position_bed',
        'heartbeat',
        'stack',
        'weight',
        'arterial_pressure',
        'pulse',
        'deviation',
        'create_at',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'patient',
                    'dyspnea',
                    'position_bed',
                    'heartbeat',
                    'stack',
                    'weight',
                    'arterial_pressure',
                    'pulse',
                    'create_at',
                ),
            }
        ),
    )

    list_filter = (
        ('create_at', DateFieldListFilter),
    )

    search_fields = (
        'patient__user__phone',
        'patient__user__first_name',
        'patient__user__last_name',
        'patient__user__middle_name',
    )

    list_select_related = ('patient',)

    resource_class = PatientIndicatorResources

    readonly_fields = ('create_at',)

    def get_patient(self, obj):
        return obj.patient.__str__()

    get_patient.short_description = 'пациент'

    def get_export_formats(self):
        """
        Return available export formats
        """
        return [base_formats.XLSX]

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()

        if request.user.is_superuser:
            return qs
        return qs.filter(
            patient__doctor=request.user.doctor
        )
