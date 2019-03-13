from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField, MonitorField
from model_utils.models import TimeStampedModel

from .utils import get_unique_slug


class BookGenre(TimeStampedModel):
    name = models.CharField(_('Genre'), blank=False, default='', max_length=112)
    slug = models.SlugField(max_length=112, unique=True)
    tracker = FieldTracker()

    class Meta:
        verbose_name = _('Book Genre')
        verbose_name_plural = _('Book Genres')

    def __str__(self):
        return f'Genre: {self.name}'

    def get_absolute_url(self):
        return reverse('books:category', kwargs={'bookgenre_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.tracker.previous('name'):
            self.slug = get_unique_slug(self.name)
        return super().save(*args, **kwargs)


class BookTag(TimeStampedModel):
    name = models.CharField(_('Tag'), blank=False, default='', max_length=112)
    slug = models.SlugField(max_length=112, unique=True)
    tracker = FieldTracker()

    class Meta:
        verbose_name = _('Book Tag')
        verbose_name_plural = _('Book Tags')

    def __str__(self):
        return f'Tag: {self.name}'

    def get_absolute_url(self):
        return reverse('books:tag', kwargs={'booktag_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.tracker.previous('name'):
            self.slug = get_unique_slug(self.name)
        return super().save(*args, **kwargs)


class Book(TimeStampedModel):
    bookgenre = models.ForeignKey(
        BookGenre,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(class)ss',
        related_query_name='%(class)s',
    )
    booktag = models.ManyToManyField(BookTag, related_name='%(class)ss')
    # volume = models.PositiveIntegerField()
    title = models.CharField(_('Title'), blank=False, default='', max_length=255)
    slug = models.SlugField(default='', max_length=255, unique=True)
    author = ArrayField(models.CharField(max_length=112), blank=True, default=list)
    country = models.CharField(default='', max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=False, default='', max_length=1024)
    chapters = models.PositiveIntegerField(_('Chapters'), blank=True, null=True, default=0)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return f'Book: {self.name}'

    def get_absolute_url(self):
        return reverse('books:book', kwargs={'book_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug or self.title != self.tracker.previous('title'):
            self.slug = get_unique_slug(self.title)
        return super().save(*args, **kwargs)


class BookChapter(TimeStampedModel):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,  # test cascade delete book or chapter
        related_name='%(class)ss',
        related_query_name='%(class)s',
    )
    title = models.CharField(_('Title'), blank=False, default='', max_length=255)
    slug = models.SlugField(default='', max_length=255, unique=True)
    text = models.TextField(blank=False, default='')

    class Meta:
        ordering = ['-created']
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')

    def __str__(self):
        return f'Chapter: {self.title}, Book: {self.book}'

    def get_absolute_url(self):
        return reverse('books:bookchapter', kwargs={
            'book_slug': self.book.slug, 'chapter_id': self.pk})

    def save(self, *args, **kwargs):
        if not self.slug or self.title != self.tracker.previous('title'):
            self.slug = get_unique_slug(self.title)
        return super().save(*args, **kwargs)


class BookVolume(TimeStampedModel):
    pass
