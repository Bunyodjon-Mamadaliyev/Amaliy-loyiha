# Generated by Django 5.2 on 2025-04-26 16:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_alter_file_category_alter_file_description_and_more'),
        ('imported', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='importeddata',
            name='columns',
            field=models.JSONField(verbose_name='columns'),
        ),
        migrations.AlterField(
            model_name='importeddata',
            name='data',
            field=models.JSONField(verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='importeddata',
            name='imported_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imports', to=settings.AUTH_USER_MODEL, verbose_name='imported by'),
        ),
        migrations.AlterField(
            model_name='importeddata',
            name='rows_count',
            field=models.PositiveIntegerField(verbose_name='rows count'),
        ),
        migrations.AlterField(
            model_name='importeddata',
            name='source_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imported_data', to='files.file', verbose_name='source file'),
        ),
    ]
