from django.urls import path

from apps.crm.views import (
    PatientListView,
    PatientDetail,
    PatientDeviationListView,
    patient_search_ajax_query,
)


urlpatterns = [
    path('', PatientListView.as_view(), name='patient_list'),
    path('<int:pk>/', PatientDetail.as_view(), name='patient_detail'),
    path(
        'patient_search_ajax_query/',
        patient_search_ajax_query,
        name='patient_search_ajax_query',
    ),
    path(
        'patient/',
        PatientDeviationListView.as_view(),
        name='deviation_list',
    )
]
