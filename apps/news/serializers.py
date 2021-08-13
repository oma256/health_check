from rest_framework import serializers
from apps.news.models import Guide
from apps.news.utils import strip_tags


class GuideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='preview')

    class Meta:
        model = Guide
        fields = ('id', 'title', 'description', 'image', 'create_at')

    def get_image(self, obj):
        if obj.preview:
            return self.context['request'].build_absolute_uri(obj.preview.url)
        return None

