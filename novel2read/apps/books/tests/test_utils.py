from django.test import TestCase

from ..utils import capitalize_slug, capitalize_str


class CapitalizeTest(TestCase):
    def setUp(self):
        self.slug = 'some-slug-123'
        self.string = 'some string 123'

    def test_capitalize_slug(self):
        self.assertEqual('Some Slug', capitalize_slug(self.slug))

    def test_capitalize_string(self):
        self.assertEqual('Some String 123', capitalize_str(self.string))
