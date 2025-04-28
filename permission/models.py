from django.db import models
from django.contrib.auth.models import User
from files.models import File


class FilePermission(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='permissions', verbose_name='file')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_permissions', verbose_name='user')
    can_view = models.BooleanField(default=False, verbose_name='can view')
    can_edit = models.BooleanField(default=False, verbose_name='can edit')
    can_delete = models.BooleanField(default=False, verbose_name='can delete')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')

    def __str__(self):
        return f"{self.user.username} uchun {self.file.title} ruxsatlari"

    class Meta:
        verbose_name = 'Fayl ruxsati'
        verbose_name_plural = 'Fayl ruxsatlari'
        unique_together = ('file', 'user')