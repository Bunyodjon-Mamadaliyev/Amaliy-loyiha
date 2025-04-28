from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponseBadRequest
from .models import ChunkedUpload
from files.models import File, FileCategory
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils import timezone
from .serializers import (ChunkedUploadSerializer, ChunkedUploadCreateSerializer,
    ChunkedUploadCompleteSerializer, FileUploadResponseSerializer,)


class ChunkedUploadStartView(generics.CreateAPIView):
    serializer_class = ChunkedUploadCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chunked_upload = serializer.save()
        response_serializer = ChunkedUploadSerializer(chunked_upload)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class ChunkedUploadChunkView(generics.UpdateAPIView):
    queryset = ChunkedUpload.objects.all()
    serializer_class = ChunkedUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'upload_id'
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            self.permission_denied(self.request)
        return obj

    def update(self, request, *args, **kwargs):
        chunked_upload = self.get_object()

        if chunked_upload.status != 'uploading':
            return Response(
                {'error': 'Upload is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )

        content_range = request.headers.get('Content-Range')
        if not content_range:
            return HttpResponseBadRequest('Content-Range header is required')

        try:
            range_info, total_size = content_range.split('/')
            range_type, range_spec = range_info.split(' ')
            start, end = map(int, range_spec.split('-'))
        except ValueError:
            return HttpResponseBadRequest('Invalid Content-Range header')

        if int(total_size) != chunked_upload.total_size:
            return HttpResponseBadRequest('Total size mismatch')

        if start != chunked_upload.offset:
            return HttpResponseBadRequest('Offset mismatch')

        chunk = request.data.get('chunk')
        if not chunk:
            return HttpResponseBadRequest('No chunk data provided')
        try:
            with open(chunked_upload.file.path, 'ab') as f:
                for chunk_part in chunk.chunks():
                    f.write(chunk_part)
        except IOError as e:
            chunked_upload.status = 'failed'
            chunked_upload.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        chunked_upload.offset = end + 1
        chunked_upload.save()
        serializer = self.get_serializer(chunked_upload)
        return Response(serializer.data)


class ChunkedUploadCompleteView(generics.CreateAPIView):
    queryset = ChunkedUpload.objects.all()
    serializer_class = ChunkedUploadCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'upload_id'

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            self.permission_denied(self.request)
        return obj

    def create(self, request, *args, **kwargs):
        chunked_upload = self.get_object()
        if chunked_upload.status != 'uploading':
            return Response(
                {'error': 'Upload is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if chunked_upload.offset != chunked_upload.total_size:
            return Response(
                {'error': 'Upload is not complete'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                original_filename = chunked_upload.filename
                file_path = default_storage.save(
                    f'files/{timezone.now().date()}/{original_filename}',
                    chunked_upload.file
                )
                file_type = 'application/octet-stream'
                file_size = chunked_upload.total_size
                file_instance = File.objects.create(
                    title=serializer.validated_data.get('title', original_filename),
                    description=serializer.validated_data.get('description', ''),
                    file=file_path,
                    file_type=file_type,
                    file_size=file_size,
                    category=serializer.validated_data.get('category'),
                    uploaded_by=request.user,
                    imported_by=request.user,
                    is_public=serializer.validated_data.get('is_public', False)
                )
                chunked_upload.status = 'completed'
                chunked_upload.save()
                response_serializer = FileUploadResponseSerializer(file_instance)
                headers = self.get_success_headers(response_serializer.data)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
        except Exception as e:
            chunked_upload.status = 'failed'
            chunked_upload.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChunkedUploadDetailView(generics.RetrieveAPIView):
    queryset = ChunkedUpload.objects.all()
    serializer_class = ChunkedUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'upload_id'

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            self.permission_denied(self.request)
        return obj
