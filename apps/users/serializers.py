from rest_framework import serializers

from apps.main.models import Helper
from apps.main.serializers import HelpersSerializer
from apps.users.models import Doctor, Patient, PatientDocument, DoctorPosition, User
from apps.users.utils import phone_regex


class AuthSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, validators=[phone_regex],)


class DoctorPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorPosition
        fields = ('name',)


class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    middle_name = serializers.CharField(source='user.middle_name')
    phone = serializers.CharField(source='user.phone')
    photo = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'phone',
            'photo',
            'positions',
        ]

    def get_photo(self, obj):
        if obj.user.photo:
            return self.context['request'].build_absolute_uri(obj.user.preview.url)
        return None

    def get_positions(self, obj):
        return [p.name for p in obj.positions.all()]


class PatientDocumentSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()

    class Meta:
        model = PatientDocument
        fields = (
            'id',
            'name',
            'image',
            'preview',
        )
        extra_kwargs = {
            'preview': {
                'read_only': True
            }
        }

    def get_preview(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.preview.url)
        return None


class PatientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    middle_name = serializers.CharField(source='user.middle_name')
    phone = serializers.CharField(source='user.phone')
    photo = serializers.SerializerMethodField()
    documents = PatientDocumentSerializer(many=True)
    doctor = DoctorSerializer()
    helpers = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'phone',
            'photo',
            'doctor',
            'date_of_birth',
            'documents',
            'address',
            'unread_notifications_exists',
            'helpers'
        ]

    def get_photo(self, obj):
        if obj.user.photo:
            return self.context['request'].build_absolute_uri(obj.user.preview.url)
        return None

    def get_helpers(self, obj):
        helpers = Helper.objects.first()
        request = self.context.get('request')
        if helpers:
            return [request.build_absolute_uri(image.image.url) for image in helpers.images.all() if image.image]
        return []


class PatientListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    middle_name = serializers.CharField(source='user.middle_name')
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'age',
            'deviation'
        ]

    @staticmethod
    def get_age(obj):
        return obj.get_age()


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['language']
        extra_kwargs = {
            'language': {
                'required': True
            }
        }
