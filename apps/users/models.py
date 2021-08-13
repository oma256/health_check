import re
from functools import reduce
from datetime import date

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from rest_framework.authtoken.models import Token

from apps.commons.constants.helpers import disable_for_loaddata
from apps.commons.constants.users import LAN_TYPE, RU
from apps.users.managers import UserManager
from apps.users.utils import phone_regex
from utils.image_upload import upload_instance_image


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name='имя', max_length=150)
    last_name = models.CharField(verbose_name='фамилия', max_length=150)
    middle_name = models.CharField(
        verbose_name='отчество',
        max_length=150,
        blank=True,
    )
    phone = models.CharField(
        verbose_name='номер телефона', max_length=17,
        validators=[phone_regex], null=True, unique=True,
    )
    photo = models.ImageField(
        verbose_name='фото',
        upload_to=upload_instance_image,
        null=True,
        blank=True,
    )
    preview = ImageSpecField(
        processors=[ResizeToFill(512, 512)],
        options={"quality": 100},
        source="photo",
        format="PNG",
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_active = models.BooleanField(verbose_name='активный', default=True)
    is_staff = models.BooleanField(verbose_name='сотрудник', default=False)
    is_doctor = models.BooleanField(verbose_name='доктор', default=False)
    is_patient = models.BooleanField(verbose_name='пациент', default=False)
    language = models.CharField(verbose_name='Язык', choices=LAN_TYPE, default=RU, max_length=8)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def get_full_name(self):
        full_name = ''
        if self.last_name:
            full_name += self.last_name

        if self.first_name:
            full_name += f' {self.first_name}'

        if self.middle_name:
            full_name += f' {self.middle_name}'

        return full_name

    @property
    def get_type(self):
        if self.is_superuser:
            return 'Администратор'
        elif self.is_staff:
            return 'Сотрудник'
        elif self.is_doctor:
            return 'Доктор'
        elif self.is_patient:
            return 'Пациент'
        return 'Пользователь'

    @property
    def get_phone_formatted(self):
        return re.sub(r'(\d{3})(\d{3})(\d{2})(\d{2})(\d{2})', r'\1 (\2) \3-\4-\5', self.phone)


@receiver(post_save, sender=User)
@disable_for_loaddata
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Patient(models.Model):
    user = models.OneToOneField(
        to='User',
        verbose_name='пользователь',
        related_name='patient',
        on_delete=models.CASCADE,
    )
    address = models.CharField(verbose_name='адрес', max_length=255, null=True)
    date_of_birth = models.DateField(verbose_name='дата рождения')
    doctor = models.ForeignKey(
        to='Doctor',
        verbose_name='доктор',
        related_name='patient',
        on_delete=models.SET_NULL,
        null=True,
    )
    weight = models.PositiveSmallIntegerField(verbose_name='вес')

    class Meta:
        verbose_name = 'пациент'
        verbose_name_plural = 'пациенты'

    def __str__(self):
        return self.user.get_full_name

    @property
    def deviation(self):
        today = date.today()
        indicator_today = self.indicator.filter(create_at__day=today.day).first()
        if indicator_today and indicator_today.deviation_count > 2:
            return True
        return False

    @property
    def unread_notifications_exists(self):
        return self.user.notifications.filter(
            create_at__date=timezone.now().today(),
            is_viewed=False
        ).order_by('notification_type', '-create_at').distinct('notification_type').exists()

    def get_age(self):
        today = date.today()
        if self.date_of_birth:
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    @property
    def get_full_amount_deviations(self):
        indicators = self.indicator.all()
        result = 0

        for indicator in indicators:
            result += indicator.deviation

        return result

    def indicator_today_filed(self):
        return self.indicator.filter(create_at__contains=timezone.now().date()).exists()


class PatientDocument(models.Model):
    patient = models.ForeignKey(
        to='Patient',
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
    )
    name = models.CharField(
        verbose_name='название документа',
        max_length=255,
        null=True
    )
    image = models.ImageField(
        verbose_name='фото',
        upload_to=upload_instance_image,
        null=True,
    )
    preview = ImageSpecField(
        processors=[ResizeToFill(512, 512)],
        options={"quality": 100},
        source="image",
        format="PNG",
    )

    class Meta:
        verbose_name = 'документ пациента'
        verbose_name_plural = 'документы пациентов'

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        to='User',
        verbose_name='пользователь',
        related_name='doctor',
        on_delete=models.CASCADE,
    )
    positions = models.ManyToManyField(
        to='DoctorPosition',
        related_name='positions',
        verbose_name='должность',
        max_length=255,
    )

    class Meta:
        verbose_name = 'доктор'
        verbose_name_plural = 'доктора'

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'


class DoctorPosition(models.Model):
    name = models.CharField(verbose_name='название', max_length=255)

    class Meta:
        verbose_name = 'должность доктора'
        verbose_name_plural = 'должности докторов'

    def __str__(self):
        return self.name
