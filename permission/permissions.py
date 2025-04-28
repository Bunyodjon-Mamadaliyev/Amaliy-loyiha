from rest_framework import permissions

class IsFileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'file'):
            return obj.file.owner == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False