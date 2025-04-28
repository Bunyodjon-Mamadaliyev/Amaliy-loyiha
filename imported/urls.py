from django.urls import path
from .views import ParseFileView, ImportedDataListView, ImportedDataDetailView, ExportDataView

urlpatterns = [
    path('files/<int:pk>/parse/', ParseFileView.as_view(), name='parse-file'),
    path('imported-data/', ImportedDataListView.as_view(), name='imported-data-list'),
    path('imported-data/<int:pk>/', ImportedDataDetailView.as_view(), name='imported-data-detail'),
    path('imported-data/<int:pk>/export/', ExportDataView.as_view(), name='export-data'),
]