from django.db import models

from utils.image_upload import upload_instance_image


class Helper(models.Model):
    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'


class HelperImages(models.Model):
    helper = models.ForeignKey(Helper, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='images')
    image = models.FileField(verbose_name='Картинка', upload_to=upload_instance_image)

    class Meta:
        verbose_name = 'Картинки'
        verbose_name_plural = 'Картинка'