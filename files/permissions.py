from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user or request.user.is_staff

class HasFileAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.uploaded_by == request.user or request.user.is_staff