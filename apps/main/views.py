from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from apps.main.models import Helper
from apps.main.serializers import HelpersSerializer


class HelperView(RetrieveAPIView):
    serializer_class = HelpersSerializer
    queryset = Helper.objects.all()

    def get_object(self):
        return self.get_queryset().first()
