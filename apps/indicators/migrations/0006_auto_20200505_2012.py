# Generated by Django 2.2.5 on 2020-05-05 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0005_auto_20200502_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientindicator',
            name='weight',
            field=models.DecimalField(decimal_places=1, max_digits=12, verbose_name='вес (кг)'),
        ),
    ]