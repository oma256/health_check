from django.db.models import Count, Case, When
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.commons.constants.notification import INDICATOR

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def get_queryset(self):
        q = self.queryset.filter(
            create_at__date=timezone.now().today(),
            user=self.request.user,
        ).order_by(
            'notification_type', '-create_at'
        ).distinct('notification_type')

        if self.request.user.patient and self.request.user.patient.indicator_today_filed():
            queryset = q.exclude(notification_type=INDICATOR)
        else:
            queryset = q

        # queryset = self.queryset.filter(
        #     create_at__date=timezone.now().today(),
        #     user=self.request.user,
        # ).annotate(
        #     indicators_count=Count(
        #         Case(
        #             When(
        #                 user__patient__indicator__create_at__contains=timezone.now().today(),
        #                 then=1
        #             )
        #         )
        #     )
        # ).exclude(
        #     indicators_count__gt=0, notification_type=INDICATOR
        # ).order_by('notification_type', '-create_at')

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        self.get_queryset().update(is_viewed=True)
        return response


class NotificationViewedUpdateAPIView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
