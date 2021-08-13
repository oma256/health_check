# Generated by Django 2.2.5 on 2020-05-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_auto_20200501_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientindicator',
            old_name='hhs',
            new_name='pulse',
        ),
        migrations.RemoveField(
            model_name='patientindicator',
            name='ad',
        ),
        migrations.AddField(
            model_name='patientindicator',
            name='arterial_pressure',
            field=models.CharField(default='', max_length=12, verbose_name='АД'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientindicator',
            name='weight',
            field=models.DecimalField(decimal_places=3, max_digits=12, verbose_name='вес (кг)'),
        ),
    ]