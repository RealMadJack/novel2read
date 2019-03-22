import pytest

from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model

from novel2read.apps.books.models import Book

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
    assert user.get_absolute_url() == f"/users/{user.username}/"


class UserReferenceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.user_1 = User.objects.create_user(username='test-1', password='test-1')
        self.test_bio = 'test bio'
        self.book = Book.objects.create(title='test book')

    def test_profile_creation_save_content(self):
        self.user.profile.bio = self.test_bio
        self.user.save()
        self.user_1.profile.bio = self.test_bio
        self.user_1.save()

        self.assertEqual(self.user.profile.bio, self.test_bio)
        self.assertEqual(self.user_1.profile.bio, self.test_bio)
        self.assertNotEqual(self.user.profile.bio, '')
        self.assertNotEqual(self.user_1.profile.bio, '')

    def test_library_creation_save_content(self):
        self.user.library.book.add(self.book)
        self.user.save()
        self.user_1.library.book.add(self.book)
        self.user_1.save()
        self.assertIn(self.book, self.user.library.book.all())
        self.assertIn(self.book, self.user_1.library.book.all())

        self.user.library.book.remove(self.book)
        self.user.save()
        self.user_1.library.book.remove(self.book)
        self.user_1.save()
        self.assertNotIn(self.book, self.user.library.book.all())
        self.assertNotIn(self.book, self.user_1.library.book.all())
