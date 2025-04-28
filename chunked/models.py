from django.db import models
from django.contrib.auth.models import User
import uuid


class ChunkedUpload(models.Model):
    UPLOAD_STATUS = (
        ('uploading', 'Yuklanmoqda'),
        ('completed', 'Yakunlandi'),
        ('failed', 'Xatolik'),
    )

    upload_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='upload id')
    file = models.FileField(upload_to='chunked_uploads/', verbose_name='file')
    filename = models.CharField(max_length=255, verbose_name='filename')
    offset = models.PositiveIntegerField(default=0, verbose_name='offset')
    total_size = models.PositiveIntegerField(verbose_name='total_size')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chunked_uploads', verbose_name='user')
    status = models.CharField(max_length=20, choices=UPLOAD_STATUS, default='uploading', verbose_name='status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')

    def __str__(self):
        return f"{self.filename} ({self.status})"

    class Meta:
        verbose_name = 'Bo\'laklab yuklash'
        verbose_name_plural = 'Bo\'laklab yuklashlar'
