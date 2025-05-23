# Generated by Django 5.2 on 2025-04-26 12:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(verbose_name="Ma'lumotlar")),
                ('rows_count', models.PositiveIntegerField(verbose_name='Qatorlar soni')),
                ('columns', models.JSONField(verbose_name='Ustunlar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('imported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imports', to=settings.AUTH_USER_MODEL, verbose_name='Import qilgan')),
                ('source_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imported_data', to='files.file', verbose_name='Manba fayl')),
            ],
            options={
                'verbose_name': "Import qilingan ma'lumot",
                'verbose_name_plural': "Import qilingan ma'lumotlar",
            },
        ),
    ]
