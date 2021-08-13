from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone

from apps.commons.constants.crm import months
from apps.crm.utils import get_month_name
from apps.indicators.models import PatientIndicator


def _get_patient_deviations(patient):
    deviation_counts = []
    deviation_days = []
    current_month = months.get(datetime.now().strftime("%B"))
    indicators = PatientIndicator.objects.filter(
        patient=patient,
        create_at__month=timezone.now().month,
    ).order_by('create_at__day')

    for indicator in indicators:
        deviation_counts.append(indicator.deviation_count)
        deviation_days.append(indicator.create_at.day)

    return deviation_counts, deviation_days, current_month


def _get_patient_deviation_by_filter(patient, time):
    if int(time) == 1:
        deviation_counts = []
        deviation_time = []
        indicators = PatientIndicator.objects.filter(
            patient=patient,
            create_at__month=timezone.now().month,
        ).order_by('create_at__day')

        for indicator in indicators:
            deviation_counts.append(indicator.deviation_count)
            deviation_time.append(indicator.create_at.day)

        return deviation_counts, deviation_time

    elif int(time) == 2:
        deviation_counts = []
        deviation_time = []
        month_before = 2
        now = datetime.utcnow()
        from_datetime = now - relativedelta(months=month_before)
        modified_from_datetime = from_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0,
        )

        indicators = PatientIndicator.objects.filter(
            patient=patient,
            create_at__gte=modified_from_datetime,
        ).annotate(month=ExtractMonth('create_at'))\
            .values('month')\
            .annotate(deviation=Sum('deviation'))\
            .values('month', 'deviation')\
            .order_by('create_at__year', 'create_at__month',)

        for indicator in indicators:
            deviation_time.append(
                months.get(get_month_name(indicator['month'])))
            deviation_counts.append(indicator['deviation'])

        return deviation_counts, deviation_time

    elif int(time) == 5:
        deviation_counts = []
        deviation_time = []
        month_before = 5
        now = datetime.utcnow()
        from_datetime = now - relativedelta(months=month_before)
        modified_from_datetime = from_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0,
        )

        indicators = PatientIndicator.objects.filter(
            patient=patient,
            create_at__gte=modified_from_datetime,
        ).annotate(month=ExtractMonth('create_at'))\
            .values('month')\
            .annotate(deviation=Sum('deviation'))\
            .values('month', 'deviation')\
            .order_by('create_at__year', 'create_at__month',)

        for indicator in indicators:
            deviation_time.append(
                months.get(get_month_name(indicator['month'])))
            deviation_counts.append(indicator['deviation'])

        return deviation_counts, deviation_time

    elif int(time) == 8:
        deviation_counts = []
        deviation_time = []
        month_before = 8
        now = datetime.utcnow()
        from_datetime = now - relativedelta(months=month_before)
        modified_from_datetime = from_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0,
        )

        indicators = PatientIndicator.objects.filter(
            patient=patient,
            create_at__gte=modified_from_datetime,
        ).annotate(month=ExtractMonth('create_at'))\
            .values('month')\
            .annotate(deviation=Sum('deviation'))\
            .values('month', 'deviation')\
            .order_by('create_at__year', 'create_at__month',)

        for indicator in indicators:
            deviation_time.append(
                months.get(get_month_name(indicator['month'])))
            deviation_counts.append(indicator['deviation'])

        return deviation_counts, deviation_time

    elif int(time) == 11:
        deviation_counts = []
        deviation_time = []
        month_before = 11
        now = datetime.utcnow()
        from_datetime = now - relativedelta(months=month_before)
        modified_from_datetime = from_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0,
        )

        indicators = PatientIndicator.objects.filter(
            patient=patient,
            create_at__gte=modified_from_datetime,
        ).annotate(month=ExtractMonth('create_at'))\
            .values('month')\
            .annotate(deviation=Sum('deviation'))\
            .values('month', 'deviation')\
            .order_by('create_at__year', 'create_at__month',)

        for indicator in indicators:
            deviation_time.append(
                months.get(get_month_name(indicator['month'])))
            deviation_counts.append(indicator['deviation'])

        return deviation_counts, deviation_time
