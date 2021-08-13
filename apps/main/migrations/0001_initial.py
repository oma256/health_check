# Generated by Django 2.2.5 on 2020-05-25 16:46

from django.db import migrations, models
import django.db.models.deletion
import utils.image_upload


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Helper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галерея',
            },
        ),
        migrations.CreateModel(
            name='HelperImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to=utils.image_upload.upload_instance_image, verbose_name='Картинка')),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.Helper', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Картинки',
                'verbose_name_plural': 'Картинка',
            },
        ),
    ]