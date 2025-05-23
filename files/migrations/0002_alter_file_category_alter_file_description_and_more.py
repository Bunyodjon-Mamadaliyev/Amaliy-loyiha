# Generated by Django 5.2 on 2025-04-26 16:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.filecategory', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='file',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='files/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_size',
            field=models.PositiveIntegerField(verbose_name='File_size'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=models.CharField(max_length=100, verbose_name='File type'),
        ),
        migrations.AlterField(
            model_name='file',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='is_public'),
        ),
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_files', to=settings.AUTH_USER_MODEL, verbose_name='uploaded_by'),
        ),
        migrations.AlterField(
            model_name='filecategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='filecategory',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='filecategory',
            name='icon',
            field=models.CharField(max_length=50, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='filecategory',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
    ]
