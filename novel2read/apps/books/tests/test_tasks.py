from celery import states
from django.test import TestCase, tag

from ..models import Book, BookGenre
from ..tasks import (
    update_book_ranking,
    book_scraper_info,
    book_scraper_chaps,
    book_scraper_chaps_update,
)


class BookTasksTest(TestCase):
    def setUp(self):
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.book = Book.objects.create(title='test book one', bookgenre=self.bookgenre, votes=134, status=1, visit_id='6831850602000905')
        self.book_1 = Book.objects.create(title='test book two', bookgenre=self.bookgenre, votes=34, status=1, visit_id='7931338406001705')
        self.book_2 = Book.objects.create(title='test book three', bookgenre=self.bookgenre, votes=74, status=1, visit_id='7176992105000305')

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

    @tag('slow')
    def test_book_scraper_initial(self):
        """
        Test celery initial scraper info + unlocked chapters
        """
        res = book_scraper_info.apply_async(args=(self.book.pk, ))
        book = Book.objects.get(pk=self.book.pk)
        book_tags = book.booktag.all()
        c_count = book.bookchapters.count()
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(book.title, "Library Of Heaven's Path")
        self.assertIn('Cultivation', [b_tag.name for b_tag in book_tags])
        self.assertIn('Weak To Strong', [b_tag.name for b_tag in book_tags])
        self.assertEqual(c_count, 0)
        self.assertTrue(book.visited)

        res = book_scraper_info.apply_async(args=(self.book.pk, ))
        self.assertEqual(res.state, states.IGNORED)

        res = book_scraper_chaps.apply_async(args=(self.book.pk, ), kwargs={'s_to': 5, })
        b_chaps = book.bookchapters.all()
        b_chaps_list = list(b_chaps)
        b_chaps_f = b_chaps_list[0]
        b_chaps_l = b_chaps_list[-1]
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(len(b_chaps_list), 5)
        self.assertEqual(b_chaps_f.slug, 'swindler')
        self.assertEqual(b_chaps_l.slug, 'young-mistress')

    # @tag('slow')
    def test_book_scraper_revisit_webnovel(self):
        self.book.visited = True
        self.book.save()
        # res = book_scraper_chaps.apply_async(args=(self.book.pk, ), kwargs={'s_to': 5, })
        self.book.refresh_from_db()
        # b_chaps = self.book.bookchapters.all()
        # b_chaps_list = list(b_chaps)
        # b_chaps_f = b_chaps_list[0]
        # b_chaps_l = b_chaps_list[-1]
        # self.assertEqual(res.state, states.SUCCESS)
        # self.assertEqual(len(b_chaps_list), 5)
        # self.assertEqual(b_chaps_f.slug, 'swindler')
        # self.assertEqual(b_chaps_l.slug, 'young-mistress')

        res = book_scraper_chaps_update.apply_async(kwargs={'s_to': 10, })
        self.assertEqual(res.state, states.SUCCESS)
