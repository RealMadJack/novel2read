from django.test import TestCase, tag

from ..models import Book, BookGenre
from ..utils import capitalize_slug, capitalize_str, multiple_replace, upload_to_s3, spoon_feed


def update_book_title(obj):
    obj.title = 'changed'
    obj.save()
    return obj


class UtilsTest(TestCase):
    def setUp(self):
        self.bookgenre = BookGenre.objects.create(name='test genre')
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

    @tag('slow')
    def test_spoon_feed(self):
        for i in range(100):
            Book.objects.create(title=f'test {i}', bookgenre=self.bookgenre)
        books = Book.objects.all()
        [i for i in spoon_feed(books, update_book_title, chunk=10)]
        Book.objects.last()
        self.assertEqual('Changed', Book.objects.first())
        self.assertEqual('Changed', Book.objects.last())
