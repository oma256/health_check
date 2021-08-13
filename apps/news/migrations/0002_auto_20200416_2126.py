# Generated by Django 2.2.5 on 2020-04-16 15:26

from django.db import migrations, models
import utils.image_upload


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='заголовок')),
                ('title_ky', models.CharField(max_length=255, null=True, verbose_name='заголовок')),
                ('description', models.TextField(verbose_name='описание')),
                ('description_ky', models.TextField(null=True, verbose_name='описание')),
                ('image', models.ImageField(null=True, upload_to=utils.image_upload.upload_instance_image, verbose_name='фото')),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'справочник',
                'verbose_name_plural': 'справочники',
            },
        ),
        migrations.DeleteModel(
            name='New',
        ),
    ]
