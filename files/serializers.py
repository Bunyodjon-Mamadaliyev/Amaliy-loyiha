from rest_framework import serializers
from .models import FileCategory, File
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.files.storage import default_storage
import os

User = get_user_model()

class FileCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileCategory
        fields = ['id', 'name', 'description', 'icon', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        return FileCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance


class FileSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    file_size_display = serializers.SerializerMethodField()
    file_type = serializers.CharField(read_only=True)
    file_size = serializers.IntegerField(read_only=True)
    imported_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = File
        fields = [
            'id', 'title', 'description', 'file', 'file_type',
            'file_size', 'file_size_display', 'category',
            'uploaded_by', 'is_public', 'imported_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'file_type', 'file_size', 'uploaded_by',
            'created_at', 'updated_at', 'file_size_display'
        ]

    def get_file_size_display(self, obj):
        if obj.file_size < 1024:
            return f"{obj.file_size} B"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.2f} KB"
        elif obj.file_size < 1024 * 1024 * 1024:
            return f"{obj.file_size / (1024 * 1024):.2f} MB"
        else:
            return f"{obj.file_size / (1024 * 1024 * 1024):.2f} GB"

    def create(self, validated_data):
        file_obj = validated_data['file']
        file_type = file_obj.content_type
        file_size = file_obj.size
        original_name = os.path.basename(file_obj.name)
        file_path = default_storage.save(f'files/{now().date()}/{original_name}', file_obj)
        file_instance = File.objects.create(
            title=validated_data.get('title', original_name),
            description=validated_data.get('description', ''),
            file=file_path,
            file_type=file_type,
            file_size=file_size,
            category=validated_data.get('category'),
            uploaded_by=self.context['request'].user,
            imported_by=validated_data.get('imported_by'),
            is_public=validated_data.get('is_public', False)
        )

        return file_instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_public = validated_data.get('is_public', instance.is_public)

        if 'category' in validated_data:
            instance.category = validated_data['category']
        if 'file' in validated_data:
            if instance.file:
                default_storage.delete(instance.file.path)

            file_obj = validated_data['file']
            file_type = file_obj.content_type
            file_size = file_obj.size
            original_name = os.path.basename(file_obj.name)
            file_path = default_storage.save(f'files/{now().date()}/{original_name}', file_obj)
            instance.file = file_path
            instance.file_type = file_type
            instance.file_size = file_size
        instance.save()
        return instance