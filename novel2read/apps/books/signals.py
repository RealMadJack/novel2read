from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book, BookChapter
from .tasks import book_scraper_initial


@receiver(post_save, sender=Book)
def update_blank_poster(sender, instance, created=False, **kwargs):
    if not instance.poster:
        instance.poster = 'posters/default.jpg'
        instance.save()


@receiver(post_save, sender=Book)
def book_scraper_initial_signal(sender, instance, created=False, **kwargs):
    if created:
        transaction.on_commit(lambda: book_scraper_initial.delay(instance.pk))


@receiver([post_save, post_delete], sender=BookChapter)
def save_book_chapters_count(sender, instance, created=False, **kwargs):
    chapters_count = instance.book.get_chapters_count()
    chapters_count_previous = instance.book.tracker.previous('chapters')
    if chapters_count != chapters_count_previous:
        instance.book.chapters = chapters_count
        instance.book.save()


@receiver(post_save, sender=BookChapter)
def create_update_chapter_cid(sender, instance, created=False, **kwargs):
    chapters_count = instance.book.get_chapters_count()
    if created:
        instance.c_id = chapters_count
        instance.save()


@receiver(post_delete, sender=BookChapter)
def delete_update_chapter_cid(sender, instance, **kwargs):
    del_cid = instance.c_id
    book_chaps = BookChapter.objects.filter(book__slug=instance.book.slug).filter(c_id__gt=del_cid)
    book_chaps.update(c_id=F('c_id') - 1)
