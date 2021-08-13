from django.urls import path

from apps.indicators.views import (
    PatientIndicatorListDetailCreateView,
    PatientIndicatorDetail,
    IndicatorToday,
)


urlpatterns = [
    path('', PatientIndicatorListDetailCreateView.as_view()),
    path('<int:pk>/', PatientIndicatorDetail.as_view()),
    path('create/', PatientIndicatorListDetailCreateView.as_view()),
    path('today/', IndicatorToday.as_view()),
]
