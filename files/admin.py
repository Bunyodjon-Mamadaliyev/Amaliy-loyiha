from django.contrib import admin
from .models import FileCategory, File

@admin.register(FileCategory)
class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'file_size', 'category', 'uploaded_by', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'uploaded_by__username')
    list_filter = ('is_public', 'category', 'created_at')
    autocomplete_fields = ['category', 'uploaded_by']