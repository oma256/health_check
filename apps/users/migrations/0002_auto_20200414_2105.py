# Generated by Django 2.2.5 on 2020-04-14 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.image_upload


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=utils.image_upload.upload_instance_image, verbose_name='фото')),
            ],
            options={
                'verbose_name': 'документ пациента',
                'verbose_name_plural': 'документы пациента',
            },
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': 'доктор', 'verbose_name_plural': 'доктора'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'пациент', 'verbose_name_plural': 'пациенты'},
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='doctor', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='patient', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='patientindicator',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicator', to='users.Patient', verbose_name='пациент'),
        ),
        migrations.AddField(
            model_name='patient',
            name='documents',
            field=models.ManyToManyField(related_name='patient_documents', to='users.PatientDocument'),
        ),
    ]
