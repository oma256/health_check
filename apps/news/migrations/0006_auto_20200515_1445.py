# Generated by Django 2.2.5 on 2020-05-15 08:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20200506_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='description_ky',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='description_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='описание'),
        ),
    ]
