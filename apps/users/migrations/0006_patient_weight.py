# Generated by Django 2.2.5 on 2020-04-23 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200416_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='вес'),
        ),
    ]
