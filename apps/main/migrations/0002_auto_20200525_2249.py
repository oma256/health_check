# Generated by Django 2.2.5 on 2020-05-25 16:49

from django.db import migrations, models
import utils.image_upload


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='helperimages',
            name='image_ky',
            field=models.FileField(null=True, upload_to=utils.image_upload.upload_instance_image, verbose_name='Картинка'),
        ),
        migrations.AddField(
            model_name='helperimages',
            name='image_ru',
            field=models.FileField(null=True, upload_to=utils.image_upload.upload_instance_image, verbose_name='Картинка'),
        ),
    ]
