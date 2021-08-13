from rest_framework import serializers

from apps.main.models import Helper


class HelpersSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Helper
        fields = [
            'images',
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all() if image.image]

