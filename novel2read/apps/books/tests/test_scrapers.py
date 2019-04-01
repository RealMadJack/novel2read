from django.test import Client, TestCase

from ..models import BookGenre, BookTag, Book
from ..scrapers import BookScraper


class BookScraperTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.scraper = BookScraper()
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.book = Book.objects.create(title='test book', bookgenre=self.bookgenre, status=0, visited_wn=False)
        self.book_1 = Book.objects.create(title='test book', bookgenre=self.bookgenre, status=0, visited_wn=True)

    def test_get_filter_db_books(self):
        books = self.scraper.get_filter_db_books()
        self.assertIn(self.book, books)
        self.assertNotIn(self.book_1, books)
