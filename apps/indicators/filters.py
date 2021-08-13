import datetime
from datetime import date

import django_filters

from apps.indicators.models import PatientIndicator


class PatientIndicatorFilter(django_filters.FilterSet):
    filter = django_filters.CharFilter(field_name='create_at', method='week_month_filter')

    class Meta:
        model = PatientIndicator
        fields = ['filter']

    def week_month_filter(self, queryset, name, value):
        today = date.today()

        if value == 'week':
            start_week = today - datetime.timedelta(today.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(create_at__range=[start_week, end_week])

        elif value == 'month':
            return queryset.filter(create_at__month=today.month)
