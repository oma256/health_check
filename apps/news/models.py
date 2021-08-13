from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField
from utils.image_upload import upload_instance_image


class Guide(models.Model):
    title = models.CharField('заголовок', max_length=255)
    description = RichTextField(verbose_name='описание')
    image = ProcessedImageField(
        verbose_name='фото',
        upload_to=upload_instance_image,
        null=True,
        blank=True,
    )
    preview = ImageSpecField(
        processors=[ResizeToFill(512, 512)],
        options={"quality": 100},
        source="image",
        format="PNG",
    )
    preview = ImageSpecField(
        processors=[ResizeToFill(512, 512)],
        options={"quality": 100},
        source="image",
        format="PNG",
    )
    create_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
        null=True,
    )

    class Meta:
        verbose_name = 'справочник'
        verbose_name_plural = 'справочники'

    def __str__(self):
        return self.title
