# Generated by Django 2.2.5 on 2020-04-14 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200414_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patientindicator',
            options={'verbose_name': 'индикатор пациента', 'verbose_name_plural': 'индикаторы пациентов'},
        ),
    ]
