import traceback
from celery import states
from celery.exceptions import Ignore
from novel2read.taskapp.celery import app, save_celery_result

from .models import Book
from .scrapers import BookScraper


@app.task(bind=True)
def update_book_ranking(self):
    try:
        books = Book.objects.published().order_by('-votes')
        # update book.ranking = 0
        # update book.ranking.f(+1)
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
        books = Book.objects.all()
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
            url_bb = scraper.url_bb[book.visit]
            book_url = f'{url_bb}{book.visit_id}'
            c_ids = scraper.wn_get_book_cids(book_url)
            c_ids = c_ids[s_from:s_to] if s_to else c_ids[s_from:]
            b_chap_info = scraper.wn_get_update_book_chaps(book, book_url, c_ids)
            b_result = '\n'.join([f'{k}: {v},' for k, v in b_chap_info.items()])
            save_celery_result(
                task_id=self.request.id,
                task_name=self.name,
                status=states.SUCCESS,
                result=f"""Updated book: {book.title}
                    {b_result}
                """,
            )
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
def book_scraper_chaps_update(self, s_from=0, s_to=0):
    books = Book.objects.filter(visited=True).exclude(visit_id__iexact='')
    for book in books:
        c_count = book.chapters_count
        s_from = c_count if c_count else s_from
        initial = True if not c_count else False
        # race condition with book_scraper_chaps(if added to que)
        to_visit = book.visit if initial else book.revisit
        to_visit_id = book.visit_id if initial else book.revisit_id
        if not book.revisited and to_visit_id:
            try:
                book.revisited = True
                book.save()
                scraper = BookScraper()
                url_bb = scraper.url_bb[to_visit]
                book_url = f'{url_bb}{to_visit_id}'
                if to_visit == 'webnovel':
                    c_ids = scraper.wn_get_book_cids(book_url)
                    c_ids = c_ids[s_from:s_to] if s_to else c_ids[s_from:]
                    b_chap_info = scraper.wn_get_update_book_chaps(book, book_url, c_ids)
                    b_result = '\n'.join([f'{k}: {v},' for k, v in b_chap_info.items()])
                    save_celery_result(
                        task_id=self.request.id,
                        task_name=self.name,
                        status=states.SUCCESS,
                        result=f"""Updated book: {book.title}
                            {b_result}
                        """,
                    )
                elif to_visit == 'boxnovel':
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
