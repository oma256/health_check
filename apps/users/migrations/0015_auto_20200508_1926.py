# Generated by Django 2.2.5 on 2020-05-08 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='documents',
        ),
        migrations.AddField(
            model_name='patientdocument',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_document', to='users.Patient'),
        ),
    ]
