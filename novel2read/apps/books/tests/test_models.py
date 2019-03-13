from django.test import TestCase
from django.urls import reverse

from ..models import BookGenre, BookTag, Book, BookChapter, BookVolume


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
        self.assertNotEqual('', reverse_url)

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
        self.assertNotEqual('', reverse_url)

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
