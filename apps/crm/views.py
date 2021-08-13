from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView

from apps.crm.permissions import DoctorRequiredMixin
from apps.crm.services import (
    _get_patient_deviations,
    _get_patient_deviation_by_filter,
)
from apps.indicators.models import PatientIndicator
from apps.users.models import Patient


class PatientListView(DoctorRequiredMixin, ListView):
    template_name = 'index.html'
    model = Patient
    queryset = Patient.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(doctor=self.request.user.doctor)


class PatientDetail(DoctorRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = Patient
    queryset = Patient.objects.all()

    def get_context_data(self, **kwargs):
        deviation_counts, \
        deviation_days, \
        current_month = _get_patient_deviations(
            patient=kwargs.get('object')
        )
        context = {
            'deviation_counts': deviation_counts,
            'deviation_days': deviation_days,
            'current_month': current_month,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(doctor=self.request.user.doctor)


class PatientDeviationListView(View):
    queryset = PatientIndicator.objects.all()

    def get(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, id=request.GET.get('patient_id'))
        deviation_counts, deviation_days = _get_patient_deviation_by_filter(
            patient=patient,
            time=request.GET.get('time'),
        )

        return JsonResponse(data={
            'deviation_counts': deviation_counts,
            'deviation_days': deviation_days,
        }, safe=False)


def patient_search_ajax_query(request):
    ctx = {}
    if request.user.is_superuser:
        patients = Patient.objects.all()
    else:
        patients = Patient.objects.filter(doctor=request.user.doctor)
    patient_data = request.GET.get('patient_data')

    if patient_data:
        filter_args = [
            Q(user__first_name__icontains=patient_data)
            | Q(user__last_name__icontains=patient_data)
            | Q(user__middle_name__icontains=patient_data)
        ]

        patients = patients.filter(*filter_args)

        if request.is_ajax():
            html = render_to_string(
                template_name="components/patient.html",
                context={"patients": patients},
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
    else:
        ctx["object_list"] = patients[:10]
        print(ctx['object_list'])
        return render(request, "index.html", context=ctx)
