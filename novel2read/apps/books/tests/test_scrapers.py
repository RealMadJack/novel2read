from django.test import Client, TestCase

from ..models import BookGenre, BookTag, Book
from ..utils import capitalize_str
from ..scrapers import BookScraper


class BookScraperTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.scraper = BookScraper()
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.booktag = BookTag.objects.create(name='test')
        self.booktag_1 = BookTag.objects.create(name='tag')
        self.book = Book.objects.create(title='test book', bookgenre=self.bookgenre, status=0, visited_wn=False)
        self.book_1 = Book.objects.create(title='test book', bookgenre=self.bookgenre, status=0, visited_wn=True)
        self.book.booktag.add(self.booktag, self.booktag_1)
        self.tags = ['test', 'tag', 'alo']
        self.chaps = [
            {'title': 'test', 'content': 'test'},
            {'title': 'test1', 'content': 'test'},
            {'title': 'test2', 'content': 'test'}
        ]
        self.wn_url = 'https://www.webnovel.com/book/11530348105422805/My-House-of-Horrors'

    def test_get_filter_db_books(self):
        books = self.scraper.get_filter_db_books()
        self.assertIn(self.book, books)
        self.assertNotIn(self.book_1, books)

    def test_create_new_tag(self):
        tag = self.scraper.create_new_tag(self.tags[0])
        tag_1 = self.scraper.create_new_tag(self.tags[1])
        tag_2 = self.scraper.create_new_tag(self.tags[2])
        self.assertFalse(tag)
        self.assertFalse(tag_1)
        self.assertEqual(capitalize_str(self.tags[2]), tag_2.name)

    def test_add_book_booktag(self):
        tag_2 = self.scraper.create_new_tag(self.tags[2])
        added = self.scraper.add_book_booktag(self.book, tag_2)
        booktags = self.book.booktag.all()
        books = tag_2.books.all()
        self.assertEqual(capitalize_str(self.tags[2]), tag_2.name)
        self.assertTrue(added)
        self.assertIn(tag_2, booktags)
        self.assertIn(self.book, books)
        self.assertEqual(booktags.count(), 3)
        added = self.scraper.add_book_booktag(self.book, tag_2)
        self.assertFalse(added)

    def test_create_book_chapter(self):
        for chap in self.chaps:
            self.scraper.create_book_chapter(
                self.book, chap['title'], chap['content'])
        bookchapters = self.book.bookchapters.all()
        self.assertEqual(bookchapters.count(), 3)
        self.assertEqual(bookchapters[1].title, capitalize_str(self.chaps[1]['title']))

    def test_wn_book_get_cids(self):
        resp = self.scraper.wn_book_get_cids(self.wn_url, s_limit=5)
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp[0], '30952845050180675')
