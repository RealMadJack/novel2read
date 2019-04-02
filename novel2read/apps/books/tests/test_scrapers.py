from django.test import Client, TestCase, tag

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
        self.wn_url = 'https://www.webnovel.com/book/11530348105422805/'
        self.wn_url_1 = 'https://www.webnovel.com/book/8360425206000005/'
        self.wn_cids = ['31433161158217963', '31434466845054269', '31435296830706024', '31456481220024926', '31457257803799212', '31458260947098371', '31478999733560367', '31479978986103973', '31481323864516947', '31502076592844451']
        self.wn_cids_1 = ['22941159621980243']

    def test_get_filter_db_books(self):
        books = self.scraper.get_filter_db_books()
        self.assertIn(self.book, books)
        self.assertNotIn(self.book_1, books)

    def test_create_book_tag(self):
        tag = self.scraper.create_book_tag(self.tags[0])
        tag_1 = self.scraper.create_book_tag(self.tags[1])
        tag_2 = self.scraper.create_book_tag(self.tags[2])
        self.assertFalse(tag)
        self.assertFalse(tag_1)
        self.assertEqual(capitalize_str(self.tags[2]), tag_2.name)

    def test_add_book_booktag(self):
        tag_2 = self.scraper.create_book_tag(self.tags[2])
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

    @tag('slow')
    def test_wn_book_get_cids(self):
        resp = self.scraper.wn_get_book_cids(self.wn_url, s_to=5)
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp[0], '30952845050180675')

    @tag('slow')
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

    @tag('slow')
    def test_wn_get_book_chaps(self):
        # big test data compatrison
        # self.wn_cids = self.scraper.wn_get_book_cids(self.wn_url)
        resp = self.scraper.wn_get_book_chaps(self.wn_url, self.wn_cids)
        resp_info = resp[-1]
        # test chap content
        for chap in resp[0:-1]:
            self.assertTrue(isinstance(chap['c_id'], int))
            self.assertTrue(isinstance(chap['c_tit'], str))
            self.assertNotEqual(chap['c_id'], 0)
            self.assertNotEqual(chap['c_tit'], 0)
            self.assertIn('<p>', chap['c_content'])
            self.assertNotIn('<p></p>', chap['c_content'])
        # test chap resp result
        self.assertTrue(isinstance(resp_info['unlocked'], int))
        self.assertTrue(isinstance(resp_info['locked'], int))
        self.assertTrue(isinstance(resp_info['locked_from_id'], int))
        self.assertTrue(isinstance(resp_info['locked_from'], str))
        self.assertNotEqual(resp_info['unlocked'], 0)
        self.assertNotEqual(resp_info['locked'], 0)
        self.assertNotEqual(resp_info['locked_from_id'], 0)
        self.assertNotEqual(len(resp_info['locked_from']), 0)

    def test_update_db_book_data(self):
        b_data = self.scraper.wn_get_book_data(self.wn_url)[0]
        b_tags = self.book.booktag.all()
        self.scraper.update_db_book_data(self.book, b_data)
        self.assertEqual(self.book.title, b_data['book_name'])
        self.assertEqual(self.book.title_sm, b_data['book_name_sm'])
        self.assertIn(b_data['book_info_author'], self.book.author)
        self.assertEqual(self.book.description, b_data['book_desc'])
        self.assertEqual(self.book.poster_url, b_data['book_poster_url'])
        self.assertEqual(self.book.rating, b_data['book_rating'])
        if b_data['chap_release'] == 'completed':
            self.assertEqual(self.book.status, 1)
        elif isinstance(b_data['chap_release'], int):
            self.assertEqual(self.book.status, 0)
            self.assertEqual(self.book.chapters_release, b_data['chap_release'])
        for tag in b_data['book_tag_list']:
            self.scraper.create_book_tag(tag)
            self.scraper.add_book_booktag(self.book, tag)
            self.assertIn(tag, [tag.name for tag in b_tags])
