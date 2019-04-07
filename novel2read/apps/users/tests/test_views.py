import pytest
from django.test import Client, TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse, resolve

from novel2read.apps.users.views import UserRedirectView, UserUpdateView
from novel2read.apps.books.models import Book

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:

    def test_get_redirect_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class LibraryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='test')
        self.user_1 = User.objects.create_user(username='testuser-1', password='test-1')
        self.book = Book.objects.create(title='test book')
        self.resp = self.client.get(reverse('users:library', kwargs={'username': self.user.username}))
        self.lib_url = reverse('users:library', kwargs={'username': self.user.username})
        self.rev_lib_add_remove = reverse('users:lib-add-remove-ajax', kwargs={'book_slug': self.book.slug})

    def test_library_response_anon(self):
        self.assertNotEqual(self.resp.status_code, 200)
        self.assertEqual(self.resp.status_code, 302)
        self.assertRedirects(
            self.resp, f'/accounts/login/?next={self.lib_url}')

    def test_lib_resp_ajax(self):
        self.client.login(username='testuser', password='test')
        resp = self.client.post(
            self.rev_lib_add_remove, {'lib_in': 0},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(
            str(resp.content, encoding='utf8'),
            {'in_lib': False, 'is_valid': True}
        )
        self.assertEqual(self.user.library.book.count(), 1)
        resp = self.client.post(
            self.rev_lib_add_remove, {'lib_in': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(
            str(resp.content, encoding='utf8'),
            {'in_lib': True, 'is_valid': True}
        )
        self.assertEqual(self.user.library.book.count(), 0)

    # def test_library_response(self):
    #     resp = self.client.post('/accounts/login/', {'username': self.user.username, 'password': self.user.password})
    #     resp = self.client.get(reverse('users:library', kwargs={'username': self.user.username}))
    #     self.assertNotEqual(resp.status_code, 302)
    #     self.assertEqual(resp.status_code, 200)
