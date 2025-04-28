from django.urls import path
from .views import (CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    FileListCreateView, FileRetrieveUpdateDestroyView,
    FileDownloadView, FileSearchView, FilesByCategoryView, MyFilesView)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('files/', FileListCreateView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-detail'),
    path('files/<int:pk>/download/', FileDownloadView.as_view(), name='file-download'),
    path('files/search/', FileSearchView.as_view(), name='file-search'),
    path('files/by-category/<int:category_id>/', FilesByCategoryView.as_view(), name='files-by-category'),
    path('files/my-files/', MyFilesView.as_view(), name='my-files'),
]