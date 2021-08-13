from django.contrib import admin
from modeltranslation.admin import TranslationStackedInline

from apps.main.models import Helper, HelperImages


class HelperImagesInline(TranslationStackedInline):
    model = HelperImages
    extra = 1


@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    inlines = [HelperImagesInline]

    def has_add_permission(self, request):
        if self.get_queryset(request).count() > 0:
            return False
        return True


