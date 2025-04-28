from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import FilePermission
from files.models import File
from .serializers import FilePermissionSerializer

class FilePermissionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FilePermissionSerializer

    def get_queryset(self):
        file_id = self.kwargs['id']
        return FilePermission.objects.filter(file_id=file_id)

    def perform_create(self, serializer):
        file_id = self.kwargs['id']
        file = get_object_or_404(File, id=file_id)
        if self.request.user != file.uploaded_by:
            return Response({'detail': 'Ruxsat berilmagan.'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(file=file)

class FilePermissionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FilePermissionSerializer
    queryset = FilePermission.objects.all()

    def check_object_permissions(self, request, obj):
        if request.user != obj.file.uploaded_by:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Faqat fayl egasi bu amalni bajara oladi.')
