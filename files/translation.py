from modeltranslation.translator import register, TranslationOptions
from .models import FileCategory, File


@register(FileCategory)
class FileCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(File)
class FileTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
