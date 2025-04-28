from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File, ImportedData
from rest_framework import parsers
from django.shortcuts import get_object_or_404
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from .permission import IsOwnerOrHasAccess
from .serializers import ParseFileSerializer, ImportedDataSerializer, ImportedDataCreateSerializer, FileSimpleSerializer


class ParseFileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrHasAccess]
    parser_classes = [parsers.JSONParser]

    def post(self, request, pk):
        file_obj = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file_obj)

        serializer = ParseFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            file_path = file_obj.file.path
            file_ext = file_path.split('.')[-1].lower()
            if file_ext in ['csv', 'txt']:
                df = pd.read_csv(
                    file_path,
                    header=serializer.validated_data.get('header_row'),
                    skiprows=serializer.validated_data.get('skip_rows', 0),
                    usecols=serializer.validated_data.get('use_columns', None),
                    dtype=str
                )
            elif file_ext in ['xls', 'xlsx']:
                df = pd.read_excel(
                    file_path,
                    sheet_name=serializer.validated_data.get('sheet_name', 0),
                    header=serializer.validated_data.get('header_row'),
                    skiprows=serializer.validated_data.get('skip_rows', 0),
                    usecols=serializer.validated_data.get('use_columns', None),
                    dtype=str
                )
            else:
                return Response(
                    {'error': 'Unsupported file format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            df = df.where(pd.notnull(df), None)
            data = df.to_dict(orient='records')
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str[:50]
            columns = list(df.columns)
            imported_data = ImportedData.objects.create(
                source_file=file_obj,
                data=data,
                rows_count=len(data),
                columns=columns,
                imported_by=request.user
            )

            response_serializer = ImportedDataSerializer(imported_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ImportedDataListView(generics.ListAPIView):
    serializer_class = ImportedDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImportedData.objects.filter(imported_by=self.request.user)


class ImportedDataDetailView(generics.RetrieveAPIView):
    queryset = ImportedData.objects.all()
    serializer_class = ImportedDataSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrHasAccess]


class ExportDataView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrHasAccess]

    def get(self, request, pk):
        imported_data = get_object_or_404(ImportedData, pk=pk)
        self.check_object_permissions(request, imported_data)
        export_format = request.query_params.get('format', 'csv').lower()

        try:
            df = pd.DataFrame(imported_data.data)

            if export_format == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="export_{pk}.csv"'
                df.to_csv(response, index=False)
                return response

            elif export_format in ['xls', 'xlsx']:
                response = HttpResponse(content_type='application/vnd.ms-excel')
                ext = 'xlsx' if export_format == 'xlsx' else 'xls'
                response['Content-Disposition'] = f'attachment; filename="export_{pk}.{ext}"'

                with BytesIO() as bio:
                    if ext == 'xlsx':
                        writer = pd.ExcelWriter(bio, engine='xlsxwriter')
                    else:
                        writer = pd.ExcelWriter(bio, engine='xlwt')

                    df.to_excel(writer, index=False, sheet_name='Exported Data')
                    writer.save()
                    response.write(bio.getvalue())

                return response

            else:
                return Response(
                    {'error': 'Unsupported export format'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )