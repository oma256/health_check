from django.urls import path

from apps.notifications.views import NotificationView, NotificationViewedUpdateAPIView

urlpatterns = [
    path('', NotificationView.as_view()),
    path('viewed/update/<int:pk>/', NotificationViewedUpdateAPIView.as_view())
]
