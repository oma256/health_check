# Generated by Django 2.2.5 on 2020-04-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200414_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdocument',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='название'),
        ),
    ]