from django.urls import path
from .views import FilePermissionListCreateAPIView, FilePermissionRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('files/<int:id>/permissions/', FilePermissionListCreateAPIView.as_view(), name='file-permission-list-create'),
    path('permissions/<int:pk>/', FilePermissionRetrieveUpdateDestroyAPIView.as_view(), name='file-permission-rud'),
]
