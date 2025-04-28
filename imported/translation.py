from modeltranslation.translator import register, TranslationOptions
from .models import ImportedData


@register(ImportedData)
class ImportedDataTranslationOptions(TranslationOptions):
    fields = ('source_file', )