import factory
from celery import states
from django.test import TestCase, tag
from django.db.models import signals

from ..models import Book, BookGenre, BookChapter
from ..tasks import (
    update_book_ranking,
    update_book_revisited,
    book_scraper_info,
    book_scraper_chaps,
    book_scraper_chaps_update,
)


class BookTasksTest(TestCase):
    @factory.django.mute_signals(signals.post_save)
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

    def test_update_book_revisited(self):
        self.book.revisited = True
        self.book.save()
        self.book_1.revisited = True
        self.book_1.save()
        self.book.refresh_from_db()
        self.book_1.refresh_from_db()
        self.assertTrue(self.book.revisited)
        self.assertTrue(self.book_1.revisited)
        res = update_book_revisited.delay()
        self.book.refresh_from_db()
        self.book_1.refresh_from_db()
        self.assertEqual(res.state, states.SUCCESS)
        self.assertFalse(self.book.revisited)
        self.assertFalse(self.book_1.revisited)

    @tag('slow')  # 30s
    def test_book_scraper_initial(self):
        """
        Test celery initial scraper info + unlocked chapters
        s_to=5 (first 5 chapters)
        """
        s_to = 5
        res = book_scraper_info.apply_async(args=(self.book.pk, ))
        self.book.refresh_from_db()
        book_tags = self.book.booktag.all()
        c_count = self.book.bookchapters.count()
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(self.book.title, "Library Of Heaven's Path")
        self.assertIn('Cultivation', [b_tag.name for b_tag in book_tags])
        self.assertIn('Weak To Strong', [b_tag.name for b_tag in book_tags])
        self.assertEqual(c_count, 0)
        self.assertTrue(self.book.visited)

        res = book_scraper_info.apply_async(args=(self.book.pk, ))
        self.assertEqual(res.state, states.IGNORED)

        res = book_scraper_chaps.apply_async(args=(self.book.pk, ), kwargs={'s_to': s_to, })
        self.book.refresh_from_db()
        b_chaps = self.book.bookchapters.all()
        b_chaps_list = list(b_chaps)
        b_chaps_f = b_chaps_list[0]
        b_chaps_l = b_chaps_list[-1]
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(len(b_chaps_list), s_to)
        self.assertEqual(b_chaps_f.slug, 'swindler')
        self.assertEqual(b_chaps_l.slug, 'young-mistress')

    @tag('slow')  # 30s
    def test_book_scraper_revisit_webnovel(self):
        s_to = 4
        self.book.visited = True
        self.book.revisit_id = self.book.visit_id
        self.book.save()
        self.book.refresh_from_db()
        BookChapter.objects.create(book=self.book, title='test 1')
        BookChapter.objects.create(book=self.book, title='test 2')
        b_chaps = self.book.bookchapters.all()
        b_chaps_list = list(b_chaps)
        b_chaps_f = b_chaps_list[0]
        b_chaps_l = b_chaps_list[-1]
        self.assertEqual(b_chaps_f.slug, 'test-1')
        self.assertEqual(b_chaps_l.slug, 'test-2')

        res = book_scraper_chaps_update.apply_async(kwargs={'s_to': s_to, })
        self.book.refresh_from_db()
        b_chaps = list(self.book.bookchapters.all())
        self.assertTrue(self.book.revisited)
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(self.book.bookchapters.count(), s_to)
        self.assertEqual(b_chaps[2].slug, 'imperfections-in-heavens-path')
        self.assertEqual(b_chaps[3].slug, 'slapping-face')

    @tag('slow')  # 30s
    def test_book_scraper_revisit_boxnovel(self):
        s_to = 4
        self.book.visited = True
        self.book.revisit = 'boxnovel'
        self.book.revisit_id = 'library-of-heavens-path'
        self.book.save()
        self.book.refresh_from_db()
        BookChapter.objects.create(book=self.book, title='test 1')
        BookChapter.objects.create(book=self.book, title='test 2')
        b_chaps = self.book.bookchapters.all()
        b_chaps_list = list(b_chaps)
        b_chaps_f = b_chaps_list[0]
        b_chaps_l = b_chaps_list[-1]
        self.assertEqual(b_chaps_f.slug, 'test-1')
        self.assertEqual(b_chaps_l.slug, 'test-2')

        res = book_scraper_chaps_update.apply_async(kwargs={'s_to': s_to, })
        # boxnovel while loop
        # res = book_scraper_chaps_update.apply_async()
        self.book.refresh_from_db()
        b_chaps = list(self.book.bookchapters.all())
        self.assertTrue(self.book.revisited)
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(self.book.bookchapters.count(), s_to)
        self.assertEqual(b_chaps[2].slug, 'imperfections-in-heavens-path')
        self.assertEqual(b_chaps[3].slug, 'slapping-face')
