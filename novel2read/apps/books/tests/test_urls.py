from django.test import TestCase
from django.urls import resolve


class BookGenreUrlTest(TestCase):
    def setUp(self):
        self.resolver_list = resolve('category/')
        self.resolver_solo = resolve('category/test-genre/')

    # def test_bookgenre_resolve(self):
    #     self.assertNotEqual(self.resolver_list.view_name, 'books:genre-all')
    #     self.assertNotEqual(self.resolver_solo.view_name, 'books:genre')

    # def test_bookgenre_resolve_invalid(self):
    #     self.assertNotEqual(self.resolver_list.view_name, '')
    #     self.assertNotEqual(self.resolver_solo.view_name, '')
