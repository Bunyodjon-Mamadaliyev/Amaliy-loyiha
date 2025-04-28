from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position')
    search_fields = ('user__username', 'department', 'position')
    list_filter = ('department',)
