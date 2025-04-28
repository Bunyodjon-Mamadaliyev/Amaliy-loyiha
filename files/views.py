from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FileCategory, File
from .serializers import FileCategorySerializer, FileSerializer
from .permissions import IsOwnerOrAdmin, HasFileAccess
from django.http import FileResponse
import os


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = FileCategory.objects.all()
    serializer_class = FileCategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileCategory.objects.all()
    serializer_class = FileCategorySerializer
    permission_classes = [permissions.IsAdminUser]

class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_public', 'uploaded_by']
    search_fields = ['title', 'description']

    def get_queryset(self):
        if self.request.user.is_staff:
            return File.objects.all()
        return File.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]


class FileDownloadView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, HasFileAccess]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file.path
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response


class FileSearchView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        return File.objects.filter(uploaded_by=self.request.user)


class FilesByCategoryView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return File.objects.filter(category_id=category_id, uploaded_by=self.request.user)


class MyFilesView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(uploaded_by=self.request.user)