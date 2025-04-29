from django.db import models
from django.contrib.auth.models import User
from files.models import File
import json

class ImportedData(models.Model):
    source_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='imported_data', verbose_name='source file')
    data = models.JSONField(verbose_name='data')
    rows_count = models.PositiveIntegerField(default=0, verbose_name='rows count')
    columns = models.JSONField(verbose_name='columns')
    imported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imports', verbose_name='imported by')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')

    class Meta:
        verbose_name = 'Import qilingan ma\'lumot'
        verbose_name_plural = 'Import qilingan ma\'lumotlar'

    def save(self, *args, **kwargs):
        if isinstance(self.data, str):
            data = json.loads(self.data)
        else:
            data = self.data

        self.rows_count = len(data)
        self.columns = list(data[0].keys()) if data else []
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.source_file.title} importi" if self.source_file else "No source file"





