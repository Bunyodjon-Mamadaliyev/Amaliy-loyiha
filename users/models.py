from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    department = models.CharField(max_length=100, verbose_name='department')
    position = models.CharField(max_length=100, verbose_name='position')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name='profile picture')

    def __str__(self):
        return f"{self.user.username} profile"

    class Meta:
        verbose_name = 'Foydalanuvchi profile'
        verbose_name_plural = 'Foydalanuvchi profillari'