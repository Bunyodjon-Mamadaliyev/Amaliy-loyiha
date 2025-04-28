from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FilePermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        ref_name = "PermissionAppUserSerializer"

class FilePermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = FilePermission
        fields = ['id', 'file', 'user', 'user_id', 'can_view', 'can_edit', 'can_delete', 'created_at']
        read_only_fields = ['id', 'file', 'user', 'created_at']


