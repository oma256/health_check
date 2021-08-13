from django.core.management import BaseCommand

from apps.indicators.models import PatientIndicator
from apps.users.models import User, Patient, Doctor, PatientDocument


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **options):
        pass