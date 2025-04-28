from django.urls import path
from .views import ChunkedUploadStartView, ChunkedUploadChunkView, ChunkedUploadCompleteView, ChunkedUploadDetailView

urlpatterns = [
    path('chunked-uploads/', ChunkedUploadStartView.as_view(), name='chunked-upload-start'),
    path('chunked-uploads/<uuid:upload_id>/', ChunkedUploadChunkView.as_view(), name='chunked-upload-chunk'),
    path('chunked-uploads/<uuid:upload_id>/complete/', ChunkedUploadCompleteView.as_view(), name='chunked-upload-complete'),
    path('chunked-uploads/<uuid:upload_id>/', ChunkedUploadDetailView.as_view(), name='chunked-upload-detail'),
]