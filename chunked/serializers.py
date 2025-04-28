from rest_framework import serializers
from .models import ChunkedUpload
from files.models import File, FileCategory


class ChunkedUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChunkedUpload
        fields = [
            'upload_id', 'filename', 'total_size', 'offset',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'upload_id', 'offset', 'status', 'created_at', 'updated_at'
        ]

class ChunkedUploadCreateSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    total_size = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        user = self.context['request'].user
        return ChunkedUpload.objects.create(
            filename=validated_data['filename'],
            total_size=validated_data['total_size'],
            user=user
        )

class ChunkedUploadCompleteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=FileCategory.objects.all(),
        required=False,
        allow_null=True
    )
    is_public = serializers.BooleanField(default=False)

class FileUploadResponseSerializer(serializers.ModelSerializer):
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            'id', 'title', 'description', 'file', 'file_type',
            'file_size', 'file_size_display', 'uploaded_by',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = fields

    def get_file_size_display(self, obj):
        if obj.file_size < 1024:
            return f"{obj.file_size} B"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.2f} KB"
        elif obj.file_size < 1024 * 1024 * 1024:
            return f"{obj.file_size / (1024 * 1024):.2f} MB"
        else:
            return f"{obj.file_size / (1024 * 1024 * 1024):.2f} GB"
