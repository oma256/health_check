from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.news.models import Guide
from apps.users.models import User, Patient, Doctor, DoctorPosition


class GuideListAPIViewTest(TestCase):
    guides_url = 'http://localhost:8000/api/v1/guides/'
    auth_url = 'http://localhost:8000/api/v1/auth/'

    def setUp(self):
        patient_user = User.objects.create(
            first_name='patient first name',
            last_name='patient last name',
            phone='+996776777777',
        )
        doctor_user = User.objects.create(
            first_name='doctor first name',
            last_name='doctor last name',
            phone='+996776999999',
        )
        position = DoctorPosition.objects.create(name='position')
        doctor = Doctor.objects.create(user=doctor_user)
        doctor.positions.add(position)
        Patient.objects.create(
            user=patient_user,
            date_of_birth=timezone.now().date(),
            doctor=doctor,
            weight='56',
        )
        Guide.objects.create(title='guide title', description='description')
        self.client = APIClient()

    def tearDown(self):
        Guide.objects.all().delete()
        DoctorPosition.objects.all().delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        User.objects.all().delete()

    def test_get_guide_list_by_unauthorized_patient_user(self):
        response = self.client.get(self.guides_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_guide_list_by_authorized_patient_user(self):
        auth_response = self.client.post(
            path=self.auth_url, data={'phone': '+996776777777'}
        )
        access_token = auth_response.json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {access_token}')

        guides_response = self.client.get(self.guides_url)

        self.assertEqual(guides_response.status_code, status.HTTP_200_OK)
        self.assertEqual(guides_response.json()[0]['title'], 'guide title')
