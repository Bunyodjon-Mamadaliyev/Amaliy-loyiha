from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from files.models import File
from .models import FilePermission

class FilePermissionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.file = File.objects.create(
            title="Test File",
            description="Test File Description",
            file=None,
            file_type="application/pdf",
            file_size=0,
            uploaded_by=self.user,
            imported_by=self.user,
            is_public=True
        )
        self.permission = FilePermission.objects.create(
            file=self.file,
            user=self.user,
            can_view=True,
            can_edit=True,
            can_delete=False
        )

    def test_file_permission_creation(self):
        self.assertEqual(self.permission.file, self.file)
        self.assertEqual(self.permission.user, self.user)
        self.assertTrue(self.permission.can_view)
        self.assertTrue(self.permission.can_edit)
        self.assertFalse(self.permission.can_delete)
        self.assertIsNotNone(self.permission.created_at)

    def test_file_permission_str(self):
        expected_str = f"{self.permission.user.username} uchun {self.permission.file.title} ruxsatlari"
        self.assertEqual(str(self.permission), expected_str)

    def test_unique_together_constraint(self):
        with self.assertRaises(IntegrityError):
            FilePermission.objects.create(
                file=self.file,
                user=self.user,
                can_view=False,
                can_edit=False,
                can_delete=False
            )
    def test_permission_fields(self):
        self.assertTrue(hasattr(self.permission, 'can_view'))
        self.assertTrue(hasattr(self.permission, 'can_edit'))
        self.assertTrue(hasattr(self.permission, 'can_delete'))
        self.assertIsInstance(self.permission.can_view, bool)
        self.assertIsInstance(self.permission.can_edit, bool)
        self.assertIsInstance(self.permission.can_delete, bool)
