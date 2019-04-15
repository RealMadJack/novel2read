from celery import states
from django.test import TestCase, tag

from ..models import Book, BookGenre
from ..tasks import (
    update_book_ranking,
    book_scraper_initial,
    book_scraper_update_info,
    book_scraper_update_chaps
)


class BookTasksTest(TestCase):
    def setUp(self):
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.book = Book.objects.create(title='test book one', bookgenre=self.bookgenre, votes=134, status=1)
        self.book_1 = Book.objects.create(title='test book two', bookgenre=self.bookgenre, votes=34, status=1)
        self.book_2 = Book.objects.create(title='test book three', bookgenre=self.bookgenre, votes=74, status=1)

    def test_update_book_ranking(self):
        self.assertEqual(self.book.ranking, 0)
        self.assertEqual(self.book_1.ranking, 0)
        self.assertEqual(self.book_2.ranking, 0)
        res = update_book_ranking.apply()
        self.book.refresh_from_db()
        self.book_1.refresh_from_db()
        self.book_2.refresh_from_db()
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(self.book.ranking, 1)
        self.assertEqual(self.book_1.ranking, 3)
        self.assertEqual(self.book_2.ranking, 2)

    # @tag('slow')
    def test_book_scraper_initial(self):
        res = book_scraper_initial.apply()
        self.assertEqual(res.state, states.SUCCESS)
