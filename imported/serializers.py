from rest_framework import serializers
from .models import ImportedData, File
from django.contrib.auth import get_user_model


User = get_user_model()

class FileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'title', 'file']

class ParseFileSerializer(serializers.Serializer):
    sheet_name = serializers.CharField(required=False, allow_null=True)
    header_row = serializers.IntegerField(default=0)
    skip_rows = serializers.IntegerField(required=False, default=0)
    use_columns = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True
    )

class ImportedDataSerializer(serializers.ModelSerializer):
    source_file = FileSimpleSerializer()
    imported_by = serializers.PrimaryKeyRelatedField(read_only=True)
    rows_count = serializers.IntegerField(read_only=True)
    columns = serializers.SerializerMethodField()

    def get_columns(self, obj):
        if isinstance(obj.columns, str):
            return obj.columns.split(',')
        return obj.columns

    class Meta:
        model = ImportedData
        fields = [
            'id', 'source_file', 'data', 'rows_count',
            'columns', 'imported_by', 'created_at'
        ]
        read_only_fields = fields



class ImportedDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportedData
        fields = ['source_file', 'data', 'rows_count', 'columns']
        read_only_fields = ['imported_by']

    def create(self, validated_data):
        validated_data['imported_by'] = self.context['request'].user
        return super().create(validated_data)