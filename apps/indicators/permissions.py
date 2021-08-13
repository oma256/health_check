from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    message = 'Вы не являетесь пациентом'

    def has_permission(self, request, view):
        return hasattr(request.user, 'patient')


class IsDoctor(BasePermission):
    message = 'Вы не являетесь доктором'

    def has_permission(self, request, view):
        return hasattr(request.user, 'doctor')
