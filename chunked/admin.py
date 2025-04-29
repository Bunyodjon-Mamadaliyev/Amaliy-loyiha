from django.contrib import admin
from .models import ChunkedUpload


@admin.register(ChunkedUpload)
class ChunkedUploadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'upload_id', 'user', 'status', 'offset', 'total_size', 'created_at')
    search_fields = ('filename', 'upload_id', 'user__username')
    list_filter = ('status', 'created_at')
