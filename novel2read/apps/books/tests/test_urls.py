from django.test import TestCase
from django.urls import resolve


class BookGenreUrlTest(TestCase):
    def setUp(self):
        self.resolver_all = resolve('/category/all/')
        self.resolver_solo = resolve('/category/test-genre/')

    def test_bookgenre_resolve(self):
        self.assertEqual(self.resolver_all.view_name, 'books:genre-all')
        self.assertEqual(self.resolver_solo.view_name, 'books:genre')

    def test_bookgenre_resolve_invalid(self):
        self.assertNotEqual(self.resolver_all.view_name, '')
        self.assertNotEqual(self.resolver_solo.view_name, '')


class BookTagUrlTest(TestCase):
    pass


class BookUrlTest(TestCase):
    def setUp(self):
        self.resolver = resolve('/books/test-book/')

    def test_book_resolve(self):
        self.assertEqual(self.resolver.view_name, 'books:book')

    def test_book_resolve_invalid(self):
        self.assertNotEqual(self.resolver.view_name, '')


class BookChapterUrlTest(TestCase):
    pass
