from django.test import TestCase

from ..utils import capitalize_slug, capitalize_str, multiple_replace


class UtilsTest(TestCase):
    def setUp(self):
        self.slug = 'some-slug-123'
        self.string = 'some string 123'
        self.to_repl = {'<p>': '', '</p>': '', '  ': '', '\n': ''}
        self.text = "'<p>\n</p>\n\n\n    \n    \nThe Sealed Classroom was a place that derwater; there was an inexplicable pressure pressing down on them, causing their breathing to become rather uneven.\n\n\n\n</p>\n<p>\n\n\n    \n    \n Youliang, should I wait for you outside? The classroom was darker than the corridor. Zhu Jianing, who stood behind Fei Youliang, had a frightened grimace on his face, and his forehead was covered with sweat.\n\n\n    \n    \n</p>"

    def test_capitalize_slug(self):
        self.assertEqual('Some Slug', capitalize_slug(self.slug))

    def test_capitalize_string(self):
        self.assertEqual('Some String 123', capitalize_str(self.string))

    def test_multiple_replace(self):
        text = multiple_replace(self.to_repl, self.text)
        self.assertNotIn('<p>', text)
        self.assertNotIn('</p>', text)
        self.assertNotIn('\n', text)
        self.assertNotIn('  ', text)
