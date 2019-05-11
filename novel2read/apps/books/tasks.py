import json
import traceback
from celery import states
from celery.exceptions import Ignore
from novel2read.taskapp.celery import app, save_celery_result
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import Book
from .scrapers import BookScraper


@app.task(bind=True)
def update_book_ranking(self):
    try:
        books = Book.objects.published().order_by('-votes')
        for i, book in enumerate(books, start=1):
            book.ranking = i
            book.save(update_fields=['ranking'])
    except Exception as exc:
        save_celery_result(
            task_id=self.request.id,
            task_name=self.name,
            status=states.FAILURE,
            result=exc,
            traceback=traceback.format_exc(),
        )
        raise Ignore()


@app.task(bind=True)
def update_book_revisited(self):
    try:
        books = Book.objects.filter(status_release=0)
        books.update(revisited=False)
    except Exception as exc:
        save_celery_result(
            task_id=self.request.id,
            task_name=self.name,
            status=states.FAILURE,
            result=exc,
            traceback=traceback.format_exc(),
        )
        raise Ignore()


@app.task(bind=True)
def book_scraper_info(self, book_id):
    """
    TODO: smart_scraper(book, url)
          if book.visit == 'webnovel'...
    """
    book = Book.objects.get(pk=book_id)
    if not book.visited and book.visit_id:
        try:
            scraper = BookScraper()
            url_bb = scraper.url_bb[book.visit]
            book_url = f'{url_bb}{book.visit_id}'
            book_data = scraper.wn_get_book_data(book_url)
            scraper.update_db_book_data(book, book_data)
            book.status = 1
            book.save()
        except Exception as exc:
            save_celery_result(
                task_id=self.request.id,
                task_name=self.name,
                status=states.FAILURE,
                result='\n'.join([f'Book: {book.title}', exc]),
                traceback=traceback.format_exc(),
            )
            raise Ignore()
    else:
        raise Ignore()


@app.task(bind=True)
def book_scraper_chaps(self, book_id, s_from=0, s_to=0):
    book = Book.objects.get(pk=book_id)
    if book.visited and book.visit_id:
        try:
            scraper = BookScraper()
            book_url = f'{scraper.url_bb[book.visit]}{book.visit_id}'
            c_ids = scraper.wn_get_book_cids(book_url)
            c_ids = c_ids[s_from:s_to] if s_to else c_ids[s_from:]
            b_chap_info = scraper.wn_get_update_book_chaps(book, book_url, c_ids)
            b_result = ' - '.join([f'{k}: {v},' for k, v in b_chap_info.items()])
            save_celery_result(
                task_id=self.request.id,
                task_name=self.name,
                status=states.SUCCESS,
                result=f'Updated book: {book.title} - {b_result}',
            )
        except Exception as exc:
            exc_result = '\n'.join([f'Book: {book.title}', f'{exc}'])
            save_celery_result(
                task_id=self.request.id,
                task_name=self.name,
                status=states.FAILURE,
                result=exc_result,
                traceback=traceback.format_exc(),
            )
            raise Ignore()
    else:
        raise Ignore()


@app.task(bind=True)
def book_revisit_novel(self, book_id, s_from=0, s_to=0):
    try:
        scraper = BookScraper()
        book = Book.objects.get(pk=book_id)
        book_url = f'{scraper.url_bb[book.revisit]}{book.revisit_id}'

        if book.revisit == 'webnovel':
            c_ids = scraper.wn_get_book_cids(book_url, s_from=s_from, s_to=s_to)
            b_chap_info = scraper.wn_get_update_book_chaps(book, book_url, c_ids)
            if b_chap_info['locked_ended_from']:
                b_result = ' - '.join([f'{k}: {v},' for k, v in b_chap_info.items()])
                save_celery_result(
                    task_id=self.request.id,
                    task_name=self.name,
                    status=states.SUCCESS,
                    result=f"Updated book: {book.title} - {b_result}",
                )
        elif book.revisit == 'boxnovel':
            b_chap_info = scraper.bn_get_update_book_chaps(book, book_url, s_to=s_to)
            if b_chap_info['updated'] >= 10:
                save_celery_result(
                    task_id=self.request.id,
                    task_name=self.name,
                    status=states.SUCCESS,
                    result=f"""
                        Updated book: {book.title};
                        Updated len: {b_chap_info['updated']}
                        Updated last: {b_chap_info['last']}
                    """,
                )
    except Exception as exc:
        exc_result = '\n'.join([f'Book: {book.title}', f'{exc}'])
        save_celery_result(
            task_id=self.request.id,
            task_name=self.name,
            status=states.FAILURE,
            result=exc_result,
            traceback=traceback.format_exc(),
        )
        raise Ignore()


@app.task(bind=True)
def book_scraper_chaps_update(self, s_from=0, s_to=0):
    books = Book.objects.filter(visited=True).exclude(visit_id__iexact='')
    interval = 15
    for book in books:
        if book.chapters_count and book.revisit_id and not book.revisited:
            try:
                interval += 5
                book.revisited = True
                book.save()
                schedule, created = IntervalSchedule.objects.get_or_create(
                    every=interval,
                    period=IntervalSchedule.SECONDS,
                )
                PeriodicTask.objects.create(
                    one_off=True,
                    interval=schedule,
                    name=f'Update book chapters: {book.title}',
                    task='novel2read.apps.books.tasks.book_revisit_novel',
                    args=json.dumps([book.pk]),
                    kwargs=json.dumps({
                        's_from': s_from,
                        's_to': s_to,
                    }),
                )
            except Exception as exc:
                exc_result = '\n'.join([f'Book: {book.title}', f'{exc}'])
                save_celery_result(
                    task_id=self.request.id,
                    task_name=self.name,
                    status=states.FAILURE,
                    result=exc_result,
                    traceback=traceback.format_exc(),
                )
                raise Ignore()
