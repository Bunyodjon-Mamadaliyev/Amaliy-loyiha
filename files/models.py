from django.db import models
from django.contrib.auth.models import User


class FileCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    description = models.TextField(verbose_name='description')
    icon = models.CharField(max_length=50, verbose_name='icon')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fayl kategoriyasi'
        verbose_name_plural = 'Fayl kategoriyalari'


class File(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    file = models.FileField(upload_to='files/', verbose_name='File')
    file_type = models.CharField(max_length=100, verbose_name='File type')
    file_size = models.PositiveIntegerField(verbose_name='File_size')
    category = models.ForeignKey(FileCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Category')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files', verbose_name='uploaded_by')
    is_public = models.BooleanField(default=False, verbose_name='is_public')
    imported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Fayl'
        verbose_name_plural = 'Fayllar'