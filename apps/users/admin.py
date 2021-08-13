from django.contrib import admin, messages
from django.contrib.admin.sites import AdminSite
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ngettext
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from apps.notifications.models import Notification
from apps.users.resources import PatientResource
from apps.users.forms import UserForm, PatientPatientForm, AdminPatientForm
from apps.users.models import (
    User, Patient, Doctor, DoctorPosition, PatientDocument
)

AdminSite.site_header = 'Администрирование CARDIO'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    readonly_fields = ['password']

    list_display = (
        'id',
        'last_name',
        'first_name',
        'middle_name',
        'phone',
        'is_patient',
        'is_doctor',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    list_filter = (
        'is_doctor',
        'is_patient',
        'is_staff',
    )

    search_fields = (
        'id',
        'first_name',
        'last_name',
        'middle_name',
        'phone'
    )

    fieldsets = (
        (None, {
            'fields': (
                'last_name',
                'first_name',
                'middle_name',
                'phone',
                'password',
                'new_password',
            ),
        }),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_superuser',
                    'is_active',
                    'is_staff',
                    'is_doctor',
                    'is_patient',
                    'groups',
                ),
            },
        )
    )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(patient__doctor=request.user.doctor)


@admin.register(Patient)
class PatientAdmin(ExportMixin, admin.ModelAdmin):

    list_display = (
        'id',
        'get_last_name',
        'get_first_name',
        'get_middle_name',
        'get_phone',
        'address',
        # 'get_photo',
        'get_weight',
        'get_documents',
        'date_of_birth',
        'get_doctor',
    )

    resource_class = PatientResource

    search_fields = (
        'id',
        'user__first_name',
        'user__last_name',
        'user__middle_name',
        'user__phone'
    )

    list_select_related = ('user',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        user = request.user
        if user.is_doctor and not user.is_superuser:
            kwargs['form'] = PatientPatientForm
        else:
            kwargs['form'] = AdminPatientForm
        return super().get_form(request, obj, change, **kwargs)

    def save_model(self, request, obj, form, change):
        if request.user.is_doctor and not request.user.is_superuser:
            obj.doctor = request.user.doctor
        super().save_model(request, obj, form, change)

    def get_export_formats(self):
        """
        Return available export formats
        """
        return [base_formats.XLSX]

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'фамилия'

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'имя'

    def get_middle_name(self, obj):
        return obj.user.middle_name

    get_middle_name.short_description = 'отчество'

    def get_phone(self, obj):
        return obj.user.phone

    get_phone.short_description = 'телефон'

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(doctor=request.user.doctor)

    # def get_photo(self, obj):
    #     if obj.user.preview:
    #         return mark_safe(
    #             f'<a href="{obj.user.preview.url}">'
    #             f'<img src="{obj.user.preview.url}" style="width: 100px;" />'
    #             f'</a>'
    #         )

    # get_photo.short_description = 'фото'

    def get_doctor(self, obj):
        if obj.doctor:
            return obj.doctor.user.get_full_name
        return 'нет доктора'

    get_doctor.short_description = 'доктор'

    def get_weight(self, obj):
        return f'{obj.weight} кг.'

    get_weight.short_description = 'вес'

    def get_documents(self, obj):
        image_list = [
            f'<a href="{d.image.url}">'
            f'<img src="{d.image.url}"'
            f'style="width: 100px; padding-top: 5px;"/>'
            f'</a>' for d in obj.documents.all() if d.image
        ]

        return mark_safe(' '.join(image_list))

    get_documents.short_description = 'документы'

    actions = ['send_indicator_notification']

    def send_indicator_notification(self, request, queryset):
        Notification.create_indicator_type(queryset=queryset)
        self.message_user(request, ngettext(
            '%d уведомление успешно отправлено.',
            '%d уведомления успешно отправлены.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    send_indicator_notification.short_description = 'Отправить уведоление для заполнения'


@admin.register(PatientDocument)
class PatientDocument(admin.ModelAdmin):

    list_display = (
        'get_patient',
        'name',
        'get_document',
    )

    search_fields = (
        'name',
        'patient__user__first_name',
        'patient__user__last_name',
        'patient__user__middle_name',
    )

    def get_document(self, obj):
        if obj.image:
            return mark_safe(
                f'<a href="{obj.image.url}">'
                f'<img src="{obj.image.url}" alt="" style="width: 100px;" />'
                f'</a>'
            )

    get_document.short_description = 'Документ'

    def get_patient(self, obj):
        return obj.patient

    get_patient.short_description = 'пациент (Ф.И.О)'

    def get_queryset(self, request):
        queryset = self.model._default_manager.get_queryset()

        if request.user.is_superuser:
            return queryset
        return queryset.filter(patient__doctor=request.user.doctor)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = (
        'get_last_name',
        'get_first_name',
        'get_middle_name',
        'get_positions',
        'get_phone',
        # 'get_photo',
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    'last_name',
                    'first_name',
                    'middle_name',
                    'phone',
                    'password',
                    'is_staff',
                    'is_doctor',
                ),
            },
        ),
    )

    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__middle_name',
    )

    list_select_related = (
        'user',
    )

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'фамилия'

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'имя'

    def get_middle_name(self, obj):
        return obj.user.middle_name

    get_middle_name.short_description = 'отчество'

    def get_positions(self, obj):
        return "\n".join([p.name for p in obj.positions.all()])

    get_positions.short_description = 'долность'

    def get_phone(self, obj):
        return obj.user.phone

    get_phone.short_description = 'телефон'

    # def get_photo(self, obj):
    #     if obj.user.preview:
    #         return mark_safe(
    #             '<img src="{url}" alt="" style="width: 100px;" />'.format(
    #                 url=obj.user.preview.url
    #             )
    #         )
    #
    # get_photo.short_description = 'фото'


@admin.register(DoctorPosition)
class DoctorPositionAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )
