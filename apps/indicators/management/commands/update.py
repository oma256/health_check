import csv
import json
from datetime import datetime

from django.core.management.base import BaseCommand

from apps.indicators.models import PatientIndicator
from apps.users.models import User, Patient


class Command(BaseCommand):
    help = 'Import PatientIndicator object form csv file'
    path = '/home/siro/Space/sunrice/cardio/cardio/indicators.patientindicator.csv'

    def handle(self, *args, **options):
        # print(PatientIndicator.objects.get(id=1098).create_at)
        object_before = 0

        self.stdout.write(
            self.style.SUCCESS('Start......'))

        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id':
                    patient_id = row[1]

                    patient = get_patient(patient_id)

                    if patient:
                        try:
                            indicator = PatientIndicator.objects.get(
                                patient=patient,
                                dyspnea=int(row[2]),
                                position_bed=int(row[3]),
                                heartbeat=int(row[4]),
                                stack=int(row[5]),
                                weight=int(row[6]),
                                arterial_pressure=str(row[7]),
                                pulse=int(row[8]),
                                deviation=int(row[9]),
                                create_at__date='2020-07-06',
                            )
                            self.stdout.write(
                                self.style.SUCCESS('Get PatientIndicator with object id%s') % indicator.id)
                            object_before = indicator.id

                            indicator.create_at = row[10]
                            # indicator.save(update_fields=['create_at'])

                        except PatientIndicator.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Cannot find PatientIndicator'))

                        except PatientIndicator.MultipleObjectsReturned:
                            self.stdout.write(self.style.ERROR(f'Get More Than 1'))
                            indicator = PatientIndicator.objects.get(id=object_before+1)
                            object_before = indicator.id

                            if indicator:
                                self.stdout.write(
                                    self.style.SUCCESS('Get by previous object =>  id%s') % indicator.id)

                                indicator.create_at = row[10]
                                # indicator.save(update_fields=['create_at'])



                    else:
                        self.stdout.write(self.style.ERROR(f'Cannot find Patient with'))
                        self.stdout.write(self.style.ERROR(f'id => {patient_id}'))

            self.stdout.write(
                self.style.SUCCESS('End......'))


def get_patient(id):
    obj = Patient.objects.filter(id=id).first()
    if obj:
        return obj
    return None

