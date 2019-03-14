from django.test import Client, TestCase
from django.urls import reverse

from ..models import BookGenre, Book


class FrontPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('books:front_page'))

    def test_frontpage_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_frontpage_response_invalid(self):
        self.assertNotEqual(self.response.status_code, 404)

    def test_frontpage_content(self):
        self.assertIn('html', self.response.content.decode('utf-8'))

    def test_frontpage_content_invalid(self):
        self.assertNotEqual(self.response.content.decode('utf-8'), {})


class GenrePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.book = Book.objects.create(title='test book', bookgenre=self.bookgenre)
        self.response_all = self.client.get(reverse('books:genre-all'))
        self.response_solo = self.client.get(
            reverse('books:genre', kwargs={'bookgenre_slug': self.bookgenre.slug}))

    def test_frontpage_response(self):
        self.assertEqual(self.response_all.status_code, 200)
        self.assertEqual(self.response_solo.status_code, 200)

    def test_frontpageresponse_invalid(self):
        self.assertNotEqual(self.response_all.status_code, 404)
        self.assertNotEqual(self.response_solo.status_code, 404)

    def test_frontpage_content(self):
        self.assertIn('html', self.response_all.content.decode('utf-8'))
        self.assertIn(self.bookgenre.name, self.response_solo.content.decode('utf-8'))

    def test_frontpage_content_invalid(self):
        self.assertNotEqual(self.response_all.content.decode('utf-8'), {})
        self.assertNotEqual(self.response_solo.content.decode('utf-8'), {})
