from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ChunkedUpload
import uuid

class ChunkedUploadModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.uploaded_file = SimpleUploadedFile(
            "chunked_testfile.txt",
            b"chunked file content",
            content_type="text/plain"
        )
        self.chunked_upload = ChunkedUpload.objects.create(
            file=self.uploaded_file,
            filename="chunked_testfile.txt",
            total_size=1024,
            user=self.user
        )

    def test_chunked_upload_creation(self):
        self.assertIsInstance(self.chunked_upload.upload_id, uuid.UUID)
        self.assertTrue(self.chunked_upload.file.name.startswith('chunked_uploads/chunked_testfile'))
        self.assertEqual(self.chunked_upload.filename, "chunked_testfile.txt")
        self.assertEqual(self.chunked_upload.offset, 0)
        self.assertEqual(self.chunked_upload.total_size, 1024)
        self.assertEqual(self.chunked_upload.user, self.user)
        self.assertEqual(self.chunked_upload.status, "uploading")
        self.assertIsNotNone(self.chunked_upload.created_at)
        self.assertIsNotNone(self.chunked_upload.updated_at)

    def test_chunked_upload_str(self):
        expected_str = f"{self.chunked_upload.filename} ({self.chunked_upload.status})"
        self.assertEqual(str(self.chunked_upload), expected_str)

    def test_chunked_upload_status_update(self):
        self.chunked_upload.status = 'completed'
        self.chunked_upload.save()
        self.assertEqual(self.chunked_upload.status, 'completed')
