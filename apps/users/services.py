
def get_user_type(user):
    return 'doctor' if user.is_doctor else 'patient'


def patient_deviation_sort(patients):
    patients_deviation_true = []
    patients_deviation_false = []

    for patient in patients:
        if patient.deviation:
            patients_deviation_true.append(patient)
        else:
            patients_deviation_false.append(patient)

    patients_deviation_true.extend(patients_deviation_false)

    return patients_deviation_true
