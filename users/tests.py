from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile_picture = SimpleUploadedFile(
            "profile_picture.jpg",
            b"image_content",
            content_type="image/jpeg"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            department="IT",
            position="Developer",
            profile_picture=self.profile_picture
        )
    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertTrue(self.user_profile.profile_picture.name.startswith('profile_pictures/profile_picture'))

    def test_user_profile_str(self):
        expected_str = f"{self.user_profile.user.username} profile"
        self.assertEqual(str(self.user_profile), expected_str)

    def test_profile_picture_optional(self):
        new_user = User.objects.create_user(username='anotheruser', password='testpassword')
        user_without_picture = UserProfile.objects.create(user=new_user)
        self.assertIsNone(user_without_picture.profile_picture.name)

    def test_unique_user_profile(self):
        with self.assertRaises(Exception):
            UserProfile.objects.create(
                user=self.user,
                department="HR",
                position="Manager"
            )
