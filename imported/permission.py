from rest_framework import permissions

class IsOwnerOrHasAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user or obj.is_public

        if hasattr(obj, 'imported_by'):
            return obj.imported_by == request.user

        if hasattr(obj, 'source_file'):
            return obj.source_file.uploaded_by == request.user or obj.source_file.is_public
        return False