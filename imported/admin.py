from django.contrib import admin
from .models import ImportedData

@admin.register(ImportedData)
class ImportedDataAdmin(admin.ModelAdmin):
    list_display = ('source_file', 'rows_count', 'imported_by', 'created_at')
    search_fields = ('source_file__title', 'imported_by__username')
    list_filter = ('created_at',)