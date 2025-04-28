from modeltranslation.translator import register, TranslationOptions
from .models import UserProfile

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('department', 'position')