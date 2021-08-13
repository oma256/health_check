from modeltranslation.translator import register, TranslationOptions

from apps.main.models import HelperImages


@register(HelperImages)
class HelperImagesTranslationOptions(TranslationOptions):
    fields = ('image',)
