from django.urls import path, include

from apps.indicators.views import (
    PatientIndicatorDetail,
    DoctorPatientIndicatorListAPI)
from apps.users.views import (
    UserAuthView,
    UserProfile,
    UserProfileListAPIView,
    DocumentListCreateAPIVIew,
    DocumentDeleteAPIView,
    FCMDeviceViewSet,
    LanguageUpdateAPIView,
    PatientRetrieveAPIView)

urlpatterns = [
    path('auth/', UserAuthView.as_view()),
    path('update/language/', LanguageUpdateAPIView.as_view()),
    path('device/', FCMDeviceViewSet.as_view({'post': 'create'}),
         name='api_register_device'),
    path('device/<registration_id>/',
         FCMDeviceViewSet.as_view({'delete': 'destroy'}),
         name='api_delete_device'),

    path('profile/', UserProfile.as_view()),
    path('doctor/', include([
        path('patients/', include([
            path('', UserProfileListAPIView.as_view()),
            path('<int:patient_id>/', include([
                path('', PatientRetrieveAPIView.as_view()),
                path('indicators/', include([
                    path('', DoctorPatientIndicatorListAPI.as_view()),
                    path('<int:indicator_id>/',
                         PatientIndicatorDetail.as_view()),
                ])),
                path('documents/', include([
                    path('', DocumentListCreateAPIVIew.as_view()),
                    path('create/', DocumentListCreateAPIVIew.as_view()),
                    path('<int:document_id>/delete/',
                         DocumentDeleteAPIView.as_view())
                ])),
            ])),

        ])),
    ])),
]
