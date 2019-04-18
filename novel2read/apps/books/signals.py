from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Book, BookChapter
from .tasks import book_scraper_info, book_scraper_chaps


@receiver(post_save, sender=Book)
def book_scraper_initial_signal(sender, instance, created=False, **kwargs):
    transaction.on_commit(
        lambda: book_scraper_info.apply_async(
            args=(instance.pk,)
        )
    )

    if created:
        transaction.on_commit(
            lambda: book_scraper_chaps.apply_async(
                args=(instance.pk,)
            )
        )


@receiver(post_save, sender=BookChapter)
def create_update_chapter_cid(sender, instance, created=False, **kwargs):
    if created:
        instance.book.update_chapters_count()
        instance.c_id = instance.book.chapters_count
        instance.save()


@receiver(post_delete, sender=BookChapter)
def delete_update_chapter_cid(sender, instance, **kwargs):
    instance.book.update_chapters_count()
    c_id_del = instance.c_id
    book_chaps = BookChapter.objects.filter(book__slug=instance.book.slug).filter(c_id__gt=c_id_del)
    book_chaps.update(c_id=F('c_id') - 1)
