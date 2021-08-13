from django.urls import path
from apps.news.views import GuideListAPIView, GuideRetrieveAPIView


urlpatterns = [
    path('', GuideListAPIView.as_view()),
    path('<int:id>', GuideRetrieveAPIView.as_view()),
]
