from import_export import resources
from import_export.fields import Field

from apps.users.models import Patient


class PatientResource(resources.ModelResource):
    user = Field(column_name='Пациент (Ф.И.О)')
    address = Field(column_name='Адрес')
    phone = Field(column_name='Контактный номер')
    date_of_birth = Field(column_name='Дата рождения')
    weight = Field(column_name='Вес')
    documents = Field(column_name='Документы')
    doctor = Field(column_name='Доктор (Ф.И.О)')

    class Meta:
        model = Patient
        fields = (
            'user', 'address', 'phone', 'date_of_birth',
            'weight', 'documents', 'doctor',
        )

    @staticmethod
    def dehydrate_doctor(instance):
        return instance.doctor.user.get_full_name

    @staticmethod
    def dehydrate_user(instance):
        return instance.user.get_full_name

    @staticmethod
    def dehydrate_documents(instance):
        return ' | '.join([d.name for d in instance.documents.all()])

    @staticmethod
    def dehydrate_address(instance):
        return instance.address

    @staticmethod
    def dehydrate_phone(instance):
        return instance.user.phone

    @staticmethod
    def dehydrate_date_of_birth(instance):
        return instance.date_of_birth.strftime('%d-%M-%Y')

    @staticmethod
    def dehydrate_weight(instance):
        return instance.weight
