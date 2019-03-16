from django.test import TestCase
from django.urls import reverse

from ..models import BookGenre, BookTag, Book, BookChapter


class BookGenreModelTest(TestCase):
    def setUp(self):
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.bookgenre_1 = BookGenre.objects.create(name='test genre')

    def test_bookgenre_data(self):
        self.assertEqual(self.bookgenre.name, 'test genre')
        self.assertEqual(self.bookgenre.slug, 'test-genre')
        self.assertEqual(self.bookgenre_1.name, 'test genre')
        self.assertEqual(self.bookgenre_1.slug, 'test-genre-1')

    def test_bookgenre_data_invalid(self):
        self.assertNotEqual(self.bookgenre.name, '')
        self.assertNotEqual(self.bookgenre.slug, '')
        self.assertNotEqual(self.bookgenre_1.name, '')
        self.assertNotEqual(self.bookgenre_1.slug, '')

    def test_bookgenre_abs_url(self):
        abs_url = self.bookgenre.get_absolute_url()
        abs_url_1 = self.bookgenre_1.get_absolute_url()
        reverse_url = reverse('books:genre', kwargs={'bookgenre_slug': self.bookgenre.slug})
        reverse_url_1 = reverse('books:genre', kwargs={'bookgenre_slug': self.bookgenre_1.slug})

        self.assertEqual(abs_url, reverse_url)
        self.assertEqual(abs_url_1, reverse_url_1)

    def test_bookgenre_abs_url_invalid(self):
        abs_url = self.bookgenre.get_absolute_url()
        reverse_url = reverse('books:genre', kwargs={'bookgenre_slug': self.bookgenre.slug})

        self.assertNotEqual(abs_url, '')
        self.assertNotEqual(reverse_url, '')

    def test_bookgenre_save_unique_slug(self):
        self.assertEqual(self.bookgenre.slug, 'test-genre')
        self.assertEqual(self.bookgenre_1.slug, 'test-genre-1')
        self.bookgenre.name = 'test new genre'
        self.bookgenre.save()
        self.bookgenre_1.name = 'test new genre'
        self.bookgenre_1.save()
        self.assertEqual(self.bookgenre.slug, 'test-new-genre')
        self.assertEqual(self.bookgenre_1.slug, 'test-new-genre-1')

    def test_bookgenre_save_unique_slug_invalid(self):
        self.assertEqual(self.bookgenre.slug, 'test-genre')
        self.assertEqual(self.bookgenre_1.slug, 'test-genre-1')
        self.bookgenre.name = 'test new genre'
        self.bookgenre.save()
        self.bookgenre_1.name = 'test new genre'
        self.bookgenre_1.save()
        self.assertNotEqual(self.bookgenre.slug, 'test-genre')
        self.assertNotEqual(self.bookgenre_1.slug, 'test-genre-1')


class BookTagModelTest(TestCase):
    def setUp(self):
        self.booktag = BookTag.objects.create(name='test tag')
        self.booktag_1 = BookTag.objects.create(name='test tag')

    def test_booktag_data(self):
        self.assertEqual(self.booktag.name, 'test tag')
        self.assertEqual(self.booktag.slug, 'test-tag')
        self.assertEqual(self.booktag_1.name, 'test tag')
        self.assertEqual(self.booktag_1.slug, 'test-tag-1')

    def test_booktag_data_invalid(self):
        self.assertNotEqual(self.booktag.name, '')
        self.assertNotEqual(self.booktag.slug, '')
        self.assertNotEqual(self.booktag_1.name, '')
        self.assertNotEqual(self.booktag_1.slug, '')

    def test_booktag_abs_url(self):
        abs_url = self.booktag.get_absolute_url()
        abs_url_1 = self.booktag_1.get_absolute_url()
        reverse_url = reverse('books:tag', kwargs={'booktag_slug': self.booktag.slug})
        reverse_url_1 = reverse('books:tag', kwargs={'booktag_slug': self.booktag_1.slug})
        self.assertEqual(abs_url, reverse_url)
        self.assertEqual(abs_url_1, reverse_url_1)

    def test_booktag_abs_url_invalid(self):
        abs_url = self.booktag.get_absolute_url()
        reverse_url = reverse('books:tag', kwargs={'booktag_slug': self.booktag.slug})
        self.assertNotEqual(abs_url, '')
        self.assertNotEqual(reverse_url, '')

    def test_booktag_save_unique_slug(self):
        self.assertEqual(self.booktag.slug, 'test-tag')
        self.assertEqual(self.booktag_1.slug, 'test-tag-1')
        self.booktag.name = 'test new tag'
        self.booktag.save()
        self.booktag_1.name = 'test new tag'
        self.booktag_1.save()
        self.assertEqual(self.booktag.slug, 'test-new-tag')
        self.assertEqual(self.booktag_1.slug, 'test-new-tag-1')

    def test_booktag_save_unique_slug_invalid(self):
        self.assertEqual(self.booktag.slug, 'test-tag')
        self.assertEqual(self.booktag_1.slug, 'test-tag-1')
        self.booktag.name = 'test new tag'
        self.booktag.save()
        self.booktag_1.name = 'test new tag'
        self.booktag_1.save()
        self.assertNotEqual(self.booktag.slug, 'test-tag')
        self.assertNotEqual(self.booktag_1.slug, 'test-tag-1')


class BookModelTest(TestCase):
    def setUp(self):
        self.bookgenre = BookGenre.objects.create(name='test genre')
        self.booktag = BookTag.objects.create(name='test tag')
        self.booktag_1 = BookTag.objects.create(name='test tag 1')
        self.book = Book.objects.create(title='test book', bookgenre=self.bookgenre)
        self.book_1 = Book.objects.create(title='test book', bookgenre=self.bookgenre)
        self.book.booktag.add(self.booktag, self.booktag_1)
        self.book_1.booktag.add(self.booktag)

    def test_book_data(self):
        self.assertEqual(self.book.title, 'test book')
        self.assertEqual(self.book.slug, 'test-book')
        self.assertEqual(self.book_1.title, 'test book')
        self.assertEqual(self.book_1.slug, 'test-book-1')

    def test_book_data_invalid(self):
        self.assertNotEqual(self.book.title, '')
        self.assertNotEqual(self.book.slug, '')
        self.assertNotEqual(self.book_1.title, '')
        self.assertNotEqual(self.book_1.slug, '')

    def test_book_abs_url(self):
        abs_url = self.book.get_absolute_url()
        abs_url_1 = self.book_1.get_absolute_url()
        reverse_url = reverse('books:book', kwargs={'book_slug': self.book.slug})
        reverse_url_1 = reverse('books:book', kwargs={'book_slug': self.book_1.slug})
        self.assertEqual(abs_url, reverse_url)
        self.assertEqual(abs_url_1, reverse_url_1)

    def test_book_abs_url_invalid(self):
        abs_url = self.book.get_absolute_url()
        reverse_url = reverse('books:book', kwargs={'book_slug': self.book.slug})
        self.assertNotEqual(abs_url, '')
        self.assertNotEqual(reverse_url, '')

    def test_book_save_unique_slug(self):
        self.assertEqual(self.book.slug, 'test-book')
        self.assertEqual(self.book_1.slug, 'test-book-1')
        self.book.title = 'test new book'
        self.book.save()
        self.book_1.title = 'test new book'
        self.book_1.save()
        self.assertEqual(self.book.slug, 'test-new-book')
        self.assertEqual(self.book_1.slug, 'test-new-book-1')

    def test_book_save_unique_slug_invalid(self):
        self.assertEqual(self.book.slug, 'test-book')
        self.assertEqual(self.book_1.slug, 'test-book-1')
        self.book.title = 'test new book'
        self.book.save()
        self.book_1.title = 'test new book'
        self.book_1.save()
        self.assertNotEqual(self.book.slug, 'test-book')
        self.assertNotEqual(self.book_1.slug, 'test-book-1')

    def test_movie_tag_m2m(self):
        book_taglist = list(self.book.booktag.all())
        book_taglist_1 = list(self.book_1.booktag.all())
        self.assertEqual(len(book_taglist), 2)
        self.assertEqual(len(book_taglist_1), 1)
        self.assertEqual(book_taglist[0].name, 'test tag')
        self.assertEqual(book_taglist[-1].name, 'test tag 1')
        self.assertEqual(book_taglist_1[0].name, 'test tag')
        # m2m remove test
        self.book.booktag.remove(book_taglist[0])
        book_taglist = list(self.book.booktag.all())
        self.assertEqual(len(book_taglist), 1)
        self.assertEqual(book_taglist[0].name, 'test tag 1')


class BookChapterTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='test book')
        self.book_1 = Book.objects.create(title='test book 1')
        self.bookchapter = BookChapter.objects.create(title='test chapter', book=self.book)
        self.bookchapter_2 = BookChapter.objects.create(title='test chapter 2', book=self.book)
        self.bookchapter_3 = BookChapter.objects.create(title='test chapter 3', book=self.book)
        self.bookchapter_1 = BookChapter.objects.create(title='test chapter', book=self.book_1)
        self.bookchapter_4 = BookChapter.objects.create(title='test chapter 4', book=self.book_1)
        self.bookchapter_5 = BookChapter.objects.create(title='test chapter 5', book=self.book_1)

    def test_book_data(self):
        self.assertEqual(self.bookchapter.title, 'test chapter')
        self.assertEqual(self.bookchapter.slug, 'test-chapter')
        self.assertEqual(self.bookchapter.book.title, 'test book')
        self.assertEqual(self.bookchapter_1.title, 'test chapter')
        self.assertEqual(self.bookchapter_1.slug, 'test-chapter-1')
        self.assertEqual(self.bookchapter_1.book.title, 'test book 1')

    def test_book_data_invalid(self):
        self.assertNotEqual(self.bookchapter.title, '')
        self.assertNotEqual(self.bookchapter.slug, '')
        self.assertNotEqual(self.bookchapter.book.title, '')
        self.assertNotEqual(self.bookchapter_1.title, '')
        self.assertNotEqual(self.bookchapter_1.slug, '')
        self.assertNotEqual(self.bookchapter_1.book.title, '')

    def test_book_abs_url(self):
        abs_url = self.bookchapter.get_absolute_url()
        abs_url_1 = self.bookchapter_1.get_absolute_url()
        reverse_url = reverse(
            'books:bookchapter',
            kwargs={'book_slug': self.book.slug, 'bookchapter_pk': self.bookchapter.pk})
        reverse_url_1 = reverse(
            'books:bookchapter',
            kwargs={'book_slug': self.book_1.slug, 'bookchapter_pk': self.bookchapter_1.pk})
        self.assertEqual(abs_url, reverse_url)
        self.assertEqual(abs_url_1, reverse_url_1)

    def test_book_abs_url_invalid(self):
        abs_url = self.book.get_absolute_url()
        reverse_url = reverse(
            'books:bookchapter',
            kwargs={'book_slug': self.book.slug, 'bookchapter_pk': self.bookchapter.pk})
        self.assertNotEqual(abs_url, '')
        self.assertNotEqual(reverse_url, '')

    # def test_chaptet_count_id_signal(self):
    #     self.assertEqual(1, self.bookchapter.inc_id)
    #     self.assertEqual(2, self.bookchapter_2.inc_id)
    #     self.assertEqual(3, self.bookchapter_3.inc_id)
    #     self.assertEqual(1, self.bookchapter_1.inc_id)
    #     self.assertEqual(2, self.bookchapter_4.inc_id)
    #     self.assertEqual(3, self.bookchapter_5.inc_id)

        # if we deleting chapter, our count changes => new chapter will not have unique id
        # if chapters > 1: prev inc_id + 1
        # self.bookchapter.delete()
        # self.bookchapter_6 = BookChapter.objects.create(title='test chapter 6', book=self.book)
        # self.assertEqual(3, self.bookchapter_3.inc_id)
        # self.assertEqual(4, self.bookchapter_6.inc_id)

    # def test_chaptet_count_id_signal_invalid(self):
    #     self.assertNotEqual(2, self.bookchapter.inc_id)
    #     self.assertNotEqual(1, self.bookchapter_2.inc_id)
    #     self.assertNotEqual(1, self.bookchapter_3.inc_id)
    #     self.assertNotEqual(0, self.bookchapter_1.inc_id)
    #     self.assertNotEqual(1, self.bookchapter_4.inc_id)
    #     self.assertNotEqual(2, self.bookchapter_5.inc_id)
    #     pass
