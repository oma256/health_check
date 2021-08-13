from django.http import Http404
from django.shortcuts import get_object_or_404
from fcm_django.api.rest_framework import (
    DeviceViewSetMixin,
    AuthorizedMixin,
    FCMDeviceSerializer,
)
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    ListCreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.users.models import User, Doctor, Patient, PatientDocument
from apps.users.serializers import (
    AuthSerializer,
    DoctorSerializer,
    PatientSerializer,
    PatientListSerializer,
    PatientDocumentSerializer,
    LanguageSerializer,
)
from apps.users.services import get_user_type, patient_deviation_sort


class UserAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(phone=request.data.get('phone'), is_active=True)
            if user.is_doctor:
                doctor = Doctor.objects.get(user=user)
                serializer = DoctorSerializer(
                    instance=doctor, context={"request": request},
                )
            else:
                patient = Patient.objects.get(user=user)
                serializer = PatientSerializer(
                    instance=patient, context={"request": request},
                )
            user_token = Token.objects.get(user=user).key
            data = {
                'token': user_token,
                'type': get_user_type(user),
                'profile': serializer.data,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Doctor.DoesNotExist, Patient.DoesNotExist):
            return Response(
                data={'detail': 'user not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientListSerializer
    queryset = Patient.objects.filter(user__is_active=True,)

    def get_queryset(self):
        patients = self.queryset.filter(doctor=self.request.user.doctor)

        return patient_deviation_sort(patients)


class UserProfile(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_doctor:
            return Doctor.objects.get(user=user)
        return Patient.objects.get(user=user)

    def get_serializer(self, *args, **kwargs):
        object = self.get_object()
        kwargs['context'] = self.get_serializer_context()
        if object.user.is_doctor:
            return DoctorSerializer(*args, **kwargs)
        return PatientSerializer(*args, **kwargs)


class PatientRetrieveAPIView(APIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Patient, user_id=kwargs.get('patient_id'))
        serializer = self.serializer_class(
            instance, context={'request': request}
        )

        return Response(serializer.data)


class LanguageUpdateAPIView(UpdateAPIView):
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class DocumentListCreateAPIVIew(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientDocumentSerializer
    queryset = PatientDocument.objects.all()

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id', None)
        if patient_id:
            return self.queryset.filter(patient__user_id=patient_id)
        return self.queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        patient = self.get_patient()
        patient.documents.add(instance)

    def get_patient(self):
        patient_id = self.kwargs.get('patient_id', None)
        patient = Patient.objects.filter(
            user_id=patient_id,
            user__is_active=True).first()
        if not patient:
            raise NotAcceptable(
                {'message': 'Пациента с данным id не '
                            'существует или он не активен'}
            )
        return patient


class DocumentDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PatientDocument.objects.all()

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id', None)
        if patient_id:
            return self.queryset.filter(patient_documents__user=patient_id)
        return self.queryset

    def get_object(self):
        document_id = self.kwargs.get('document_id', None)
        if document_id:
            document = self.get_queryset().filter(id=document_id).first()
            if document:
                return document
            raise Http404

        return super().get_object()


class FCMDeviceViewSet(AuthorizedMixin, DeviceViewSetMixin, ModelViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer

    def get_object(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        device = self.get_queryset().filter(device_id=self.request.POST.get('device_id', None)).first()
        if device:
            return Response(self.get_serializer(device).data, status=status.HTTP_200_OK)
        return super(FCMDeviceViewSet, self).create(request, *args, **kwargs)
