from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from apps.news.models import Guide


@admin.register(Guide)
class NewsAdmin(TranslationAdmin):
    list_display = [
        'title',
        'get_description',
        'get_image',
        'get_create_at'
    ]

    fieldsets = [
        (u'новости', {'fields': ('title', 'description', 'image')})
    ]

    actions = None

    list_filter = ('create_at',)

    def get_create_at(self, obj):
        return obj.create_at.strftime('%d-%m-%Y %H:%M:%S')

    get_create_at.short_description = 'дата создания'

    def get_image(self, obj):
        if obj.preview:
            return mark_safe(
                f'<img src="{obj.preview.url}" alt="" style="width: 100px;" />'
            )
        return "-"

    get_image.short_description = "изображение"

    def get_description(self, obj):
        return mark_safe(obj.description[:100] + '...')

    get_description.short_description = 'описание'
