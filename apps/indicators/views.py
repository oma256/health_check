from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.indicators.filters import PatientIndicatorFilter
from apps.indicators.models import PatientIndicator
from apps.indicators.permissions import IsPatient, IsDoctor
from apps.indicators.serializers import (
    PatientIndicatorSerializer,
    PatientIndicatorDetailSerializer,
    DoctorPatientIndicatorHistory,
)


class PatientIndicatorListDetailCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsPatient)
    serializer_class = PatientIndicatorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientIndicatorFilter
    queryset = PatientIndicator.objects.all()
    lookup_url_kwarg = 'patient_id'

    def get_queryset(self):
        patient_id = self.kwargs.get(self.lookup_url_kwarg)
        if patient_id:
            return self.queryset.filter(
                patient__user=patient_id
            ).order_by('-create_at')[:10]

        return self.queryset.filter(patient=self.request.user.patient)


class PatientIndicatorDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientIndicatorDetailSerializer
    queryset = PatientIndicator.objects.all()

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id', None)
        if patient_id:
            return self.queryset.filter(patient=patient_id)
        return self.queryset.filter(patient=self.request.user.patient)

    def get_object(self):
        indicator_id = self.kwargs.get('indicator_id', None)
        if indicator_id:
            indicator = self.queryset.filter(pk=indicator_id).first()
            if indicator:
                return indicator
            raise Http404

        return super().get_object()


class IndicatorToday(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        indicator = PatientIndicator.objects.filter(
            create_at__contains=timezone.now().date(),
            patient=request.user.patient,
        ).first()
        return Response(
            {
                "id": getattr(indicator, 'id', None),
                "isTodaySend": indicator is not None
            }
        )


class DoctorPatientIndicatorListAPI(ListAPIView):
    permission_classes = (IsAuthenticated, IsDoctor)
    serializer_class = DoctorPatientIndicatorHistory
    queryset = PatientIndicator.objects.all()
    lookup_url_kwarg = 'patient_id'

    def get_queryset(self):
        patient_id = self.kwargs.get(self.lookup_url_kwarg)
        if patient_id:
            return self.queryset.filter(
                patient__user=patient_id
            ).order_by('-create_at')[:10]

        return self.queryset.filter(patient=self.request.user.patient)
