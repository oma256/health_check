# Generated by Django 2.2.5 on 2020-05-08 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200508_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdocument',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='users.Patient'),
        ),
    ]
