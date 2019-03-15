from django.test import Client, TestCase
from django.urls import reverse

from ..models import BookGenre, BookTag, Book


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
        self.bookgenre_1 = BookGenre.objects.create(name='test genre other')
        self.book = Book.objects.create(title='test book', bookgenre=self.bookgenre)
        self.book_1 = Book.objects.create(title='test book other', bookgenre=self.bookgenre_1)
        self.response_all = self.client.get(reverse('books:genre-list'))
        self.response_solo = self.client.get(
            reverse('books:genre', kwargs={'bookgenre_slug': self.bookgenre.slug}))

    def test_frontpage_response(self):
        self.assertEqual(self.response_all.status_code, 200)
        self.assertEqual(self.response_solo.status_code, 200)

    def test_frontpage_response_invalid(self):
        self.assertNotEqual(self.response_all.status_code, 404)
        self.assertNotEqual(self.response_solo.status_code, 404)

    def test_frontpage_content(self):
        self.assertIn('html', self.response_all.content.decode('utf-8'))
        self.assertIn(self.bookgenre.name, self.response_solo.content.decode('utf-8'))
        self.assertIn(self.book.title, self.response_all.content.decode('utf-8'))
        self.assertIn(self.book_1.title, self.response_all.content.decode('utf-8'))
        self.assertIn(self.book.title, self.response_solo.content.decode('utf-8'))
        self.assertNotIn(self.book_1.title, self.response_solo.content.decode('utf-8'))

    def test_frontpage_content_invalid(self):
        self.assertNotEqual(self.response_all.content.decode('utf-8'), {})
        self.assertNotEqual(self.response_solo.content.decode('utf-8'), {})


class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.booktag = BookTag.objects.create(name='test tag')
        self.book = Book.objects.create(title='test book', bookgenre=self.bookgenre)
        self.book.booktag.add(self.booktag)
        self.response = self.client.get(reverse('books:book', kwargs={'book_slug': self.book.slug}))

    def test_book_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_book_response_invalid(self):
        self.assertNotEqual(self.response.status_code, 404)

    def test_book_content(self):
        self.assertIn('html', self.response.content.decode('utf-8'))
        self.assertIn(self.book.bookgenre.name, self.response.content.decode('utf-8'))
        self.assertIn(self.book.title, self.response.content.decode('utf-8'))
        self.assertIn(self.booktag.name, self.response.content.decode('utf-8'))
