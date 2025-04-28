from django.contrib import admin
from .models import FilePermission

@admin.register(FilePermission)
class FilePermissionAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'can_view', 'can_edit', 'can_delete', 'created_at')
    search_fields = ('file__title', 'user__username')
    list_filter = ('can_view', 'can_edit', 'can_delete')