from django.test import TestCase
from django.contrib.auth.models import User
from .models import FileCategory, File
from django.core.files.uploadedfile import SimpleUploadedFile

class FileCategoryModelTest(TestCase):

    def setUp(self):
        self.category = FileCategory.objects.create(
            name="Test Category",
            description="Test Description",
            icon="test-icon"
        )

    def test_filecategory_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test Description")
        self.assertEqual(self.category.icon, "test-icon")
        self.assertIsNotNone(self.category.created_at)

    def test_filecategory_str(self):
        self.assertEqual(str(self.category), "Test Category")


class FileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = FileCategory.objects.create(
            name="Test Category",
            description="Test Description",
            icon="test-icon"
        )
        self.uploaded_file = SimpleUploadedFile(
            "testfile.txt",
            b"file_content",
            content_type="text/plain"
        )
        self.file = File.objects.create(
            title="Test File",
            description="Test Description",
            file=self.uploaded_file,
            file_type="text/plain",
            file_size=1234,
            category=self.category,
            uploaded_by=self.user,
            imported_by=self.user,
            is_public=True
        )

    def test_file_creation(self):
        self.assertEqual(self.file.title, "Test File")
        self.assertEqual(self.file.description, "Test Description")
        self.assertTrue(self.file.file.name.startswith('files/testfile'))
        self.assertEqual(self.file.file_type, "text/plain")
        self.assertEqual(self.file.file_size, 1234)
        self.assertEqual(self.file.category, self.category)
        self.assertEqual(self.file.uploaded_by, self.user)
        self.assertEqual(self.file.imported_by, self.user)
        self.assertTrue(self.file.is_public)
        self.assertIsNotNone(self.file.created_at)
        self.assertIsNotNone(self.file.updated_at)

    def test_file_str(self):
        self.assertEqual(str(self.file), "Test File")
