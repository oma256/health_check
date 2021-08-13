from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.news.models import Guide
from apps.news.serializers import GuideSerializer


class GuideListAPIView(ListAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = (IsAuthenticated,)


class GuideRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = (IsAuthenticated,)

    # TODO
    # def get_object(self):
    #     try:
    #         obj = Guide.objects.get(id=self.request.GET.get('id'))
    #         print(obj)
    #     except Guide.DoesNotExist:
    #         return None
    #     self.check_object_permissions(self.request, obj)
    #
    #     return obj
    #
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     if instance is None:
    #         return Response(
    #             data={'detail': 'guide does not exist.'},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
