from django.urls import path

from apps.main.views import HelperView

urlpatterns = [
    path('helpers/', HelperView.as_view()),
]
