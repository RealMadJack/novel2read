from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
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
        ordering = ['name']
        verbose_name = _('Book Genre')
        verbose_name_plural = _('Book Genres')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:genre', kwargs={'bookgenre_slug': self.slug})

    def save(self, *args, **kwargs):
        self.name = ' '.join([w.capitalize() for w in self.name.split(' ')])
        if not self.slug or self.name != self.tracker.previous('name'):
            self.slug = get_unique_slug(BookGenre, self.name)
        return super().save(*args, **kwargs)


class BookTag(TimeStampedModel):
    name = models.CharField(_('Tag'), blank=False, default='', max_length=112)
    slug = models.SlugField(max_length=112, unique=True)
    tracker = FieldTracker()

    class Meta:
        ordering = ['name']
        verbose_name = _('Book Tag')
        verbose_name_plural = _('Book Tags')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:tag', kwargs={'booktag_slug': self.slug})

    def save(self, *args, **kwargs):
        self.name = ' '.join([w.capitalize() for w in self.name.split(' ')])
        if not self.slug or self.name != self.tracker.previous('name'):
            self.slug = get_unique_slug(BookTag, self.name)
        return super().save(*args, **kwargs)


class Book(TimeStampedModel):
    bookgenre = models.ForeignKey(
        BookGenre,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(class)ss',
        related_query_name='%(class)s',
    )
    booktag = models.ManyToManyField(BookTag, related_name='%(class)ss', blank=True)
    title = models.CharField(_('Title'), blank=False, default='', max_length=255)
    title_sm = models.CharField(_('Title short'), blank=True, default='', max_length=50)
    slug = models.SlugField(default='', max_length=255, unique=True)
    author = ArrayField(models.CharField(max_length=112), blank=True, default=list)
    country = models.CharField(default='', max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True, default='', max_length=1024)
    chapters = models.PositiveIntegerField(_('Chapters'), blank=True, null=True, default=0)
    chapters_max = models.PositiveIntegerField(_('Chapters Full'), blank=True, null=True, default=0)
    chapters_release = models.SmallIntegerField(_('Chapters update'), blank=True, null=True, default=0)
    # poster = models.URLField(_('Poster'), blank=True, null=True, upload_to='posters')
    poster_url = models.URLField(_('Poster URL'), blank=True, default='https://media.istockphoto.com/vectors/blank-book-cover-vector-id466036957?k=6&m=466036957&s=612x612&w=0&h=SHDzHMVV6CHMNk6P-7igrYcZTfGryYdk_J7jzf7MwyY=', max_length=255)
    volumes = ArrayField(models.SmallIntegerField(default=0), blank=True, default=list)
    votes = models.PositiveIntegerField(_('Votes'), blank=True, null=True, default=0)
    votes_external = models.PositiveIntegerField(
        _('Votes External'), blank=True, null=True, default=0)
    rating = models.FloatField(_('Rating'), blank=True, default=0.0)
    ranking = models.PositiveIntegerField(_('Ranking'), blank=True, null=True, default=0)
    visited_wn = models.BooleanField(_('WN scraped'), default=False)
    locked_wn = models.IntegerField(_('WN locked from'), blank=True, null=True, default=0)
    visited_bn = models.BooleanField(_('BN scraped'), default=False)
    book_id_wn = models.BigIntegerField(_('WN book id'), blank=True, null=True, default=0)
    book_id_bn = models.CharField(_('BN book id'), blank=True, default='', max_length=255)
    STATUS = Choices(
        (0, 'draft', _('draft')),
        (1, 'published', _('published')),
    )
    status = models.IntegerField(choices=STATUS, default=STATUS.published)
    STATUS_RELEASE = Choices(
        (0, 'ongoing', _('ongoing')),
        (1, 'completed', _('completed')), )
    status_release = models.IntegerField(choices=STATUS_RELEASE, default=STATUS_RELEASE.ongoing)
    published_at = MonitorField(monitor='status', when=['published'])
    tracker = FieldTracker()

    class Meta:
        ordering = ['-created']
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book', kwargs={'book_slug': self.slug})

    def save(self, *args, **kwargs):
        self.title = ' '.join([w.capitalize() for w in self.title.split(' ')])
        if not self.slug or self.title != self.tracker.previous('title'):
            self.slug = get_unique_slug(Book, self.title)
        return super().save(*args, **kwargs)

    def get_chapters_count(self):
        return self.bookchapters.count()


class BookChapter(TimeStampedModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,  # test cascade delete book or chapter
        related_name='%(class)ss',
        related_query_name='%(class)s',
    )
    # count_id = models.PositiveIntegerField(default=1, blank=True, null=True, db_index=True)
    title = models.CharField(_('Title'), blank=False, default='', max_length=255)
    slug = models.SlugField(default='', max_length=255, unique=True)
    text = models.TextField(blank=False, default='')
    tracker = FieldTracker()

    class Meta:
        ordering = ['pk']
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')

    def __str__(self):
        return f'Book: {self.book.title} - Chapter: {self.title}'

    def get_absolute_url(self):
        return reverse('books:bookchapter', kwargs={
            'book_slug': self.book.slug, 'bookchapter_pk': self.pk})

    def save(self, *args, **kwargs):
        self.title = ' '.join([w.capitalize() for w in self.title.split(' ')])
        if not self.slug or self.title != self.tracker.previous('title'):
            self.slug = get_unique_slug(BookChapter, self.title)
        return super().save(*args, **kwargs)


@receiver([post_save, post_delete], sender=BookChapter)
def save_book_chapters_count(sender, instance, created=False, **kwargs):
    chapters_count = instance.book.get_chapters_count()
    chapters_count_previous = instance.book.tracker.previous('chapters')
    if chapters_count != chapters_count_previous:
        instance.book.chapters = chapters_count
        instance.book.save()
