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
        self.wn_cids = ['31433161158217963', '31434466845054269', '31435296830706024', '31456481220024926', '31457257803799212', '31458260947098371', '31478999733560367', '31479978986103973', '31481323864516947', '31502076592844451']

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

    # def test_wn_book_get_cids(self):
    #     resp = self.scraper.wn_get_book_cids(self.wn_url, s_to=5)
    #     self.assertEqual(len(resp), 5)
    #     self.assertEqual(resp[0], '30952845050180675')

    def test_wn_get_book_data(self):
        resp = self.scraper.wn_get_book_data(self.wn_url)[0]
        self.assertTrue(isinstance(resp['book_desc'], str))
        self.assertTrue(isinstance(resp['book_name'], str))
        self.assertTrue(isinstance(resp['book_name_sm'], str))
        self.assertTrue(isinstance(resp['book_info_genre'], str))
        self.assertTrue(isinstance(resp['chap_release'], int))
        self.assertTrue(isinstance(resp['book_info_chap_count'], int))
        self.assertTrue(isinstance(resp['book_info_author'], str))
        self.assertTrue(isinstance(resp['book_rating'], float))
        self.assertTrue(isinstance(resp['book_poster_url'], str))
        self.assertTrue(isinstance(resp['book_tag_list'], list))
        self.assertIn('<p>', resp['book_desc'])
        self.assertNotEqual(len(resp['book_name']), 0)
        self.assertNotEqual(len(resp['book_name_sm']), 0)
        self.assertNotEqual(resp['book_info_chap_count'], 0)
        self.assertNotEqual(len(resp['book_info_genre']), 0)
        self.assertNotEqual(len(resp['book_info_author']), 0)
        self.assertNotEqual(len(resp['book_poster_url']), 0)
        self.assertNotEqual(len(resp['book_tag_list']), 0)

    def test_wn_book_get_chaps(self):
        resp = self.scraper.wn_book_get_chaps(self.wn_url)
