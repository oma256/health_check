from modeltranslation.translator import register, TranslationOptions

from apps.news.models import Guide


@register(Guide)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
