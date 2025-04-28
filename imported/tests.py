from django.test import TestCase
from django.contrib.auth.models import User
from .models import ImportedData
from files.models import File
import json

class ImportedDataModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.file = File.objects.create(
            title="Test File",
            description="Test File Description",
            file=None,
            file_type="application/json",
            file_size=0,
            uploaded_by=self.user,
            imported_by=self.user,
            is_public=True
        )
        self.imported_data = ImportedData.objects.create(
            source_file=self.file,
            data=json.dumps([{"column1": "value1", "column2": "value2"}]),
            imported_by=self.user
        )

    def test_imported_data_creation(self):
        self.assertEqual(self.imported_data.source_file, self.file)
        self.assertEqual(self.imported_data.rows_count, 1)
        self.assertEqual(self.imported_data.columns, ["column1", "column2"])
        self.assertEqual(self.imported_data.imported_by, self.user)
        self.assertIsNotNone(self.imported_data.created_at)

    def test_imported_data_str(self):
        expected_str = f"{self.imported_data.source_file.title} importi"
        self.assertEqual(str(self.imported_data), expected_str)

    def test_rows_count_property(self):
        self.imported_data.data = json.dumps([{"column1": "value1", "column2": "value2"}, {"column1": "value3", "column2": "value4"}])
        self.imported_data.save()
        self.assertEqual(self.imported_data.rows_count, 2)

    def test_columns_property(self):
        self.imported_data.data = json.dumps([{"column1": "value1", "column2": "value2"}])
        self.imported_data.save()
        self.assertEqual(self.imported_data.columns, ["column1", "column2"])
