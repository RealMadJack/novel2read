import traceback
from celery import states
from celery.exceptions import Ignore
from novel2read.taskapp.celery import app, save_celery_result

from .models import Book
from .scrapers import BookScraper


@app.task(bind=True)
def debug_task_test(self):
    """
    result = AsyncResult(self.request.id)
    if result.state in READY_STATES | EXCEPTION_STATES:
    if result.state == 'FAILURE' or (result.state == 'SUCCESS' and result.get() == 'FAILURE'):
        raise Ignore()

    some_state = True
    if some_state:
        self.update_state(
            state=states.FAILURE,
            meta='REASON FOR FAILURE'
        )
        raise Ignore()

    try:
        raise ValueError('Some error')
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
                'custom': '...'
            })
        raise Ignore()

    save_celery_result(self.request.id, self.name)
    """
    print(f"task every 10 sec")


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
                result=exc,
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
            bookchaps = scraper.wn_get_book_chaps(book_url, c_ids)
            scraper.create_update_db_book_chaps(book, bookchaps)
        except Exception as exc:
            save_celery_result(
                task_id=self.request.id,
                task_name=self.name,
                status=states.FAILURE,
                result=exc,
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
        to_visit = book.visit if initial else book.revisit
        to_visit_id = book.visit_id if initial else book.revisit_id
        if not book.revisited and to_visit_id:
            try:
                book.revisited = True
                book.save()
                scraper = BookScraper()
                url_bb = scraper.url_bb[to_visit]
                if to_visit == 'webnovel':
                    book_url = f'{url_bb}{to_visit_id}'
                    c_ids = scraper.wn_get_book_cids(book_url)
                    c_ids = c_ids[s_from:s_to] if s_to else c_ids[s_from:]
                    bookchaps = scraper.wn_get_book_chaps(book_url, c_ids)
                    scraper.create_update_db_book_chaps(book, bookchaps)
                    save_celery_result(
                        task_id=self.request.id,
                        task_name=self.name,
                        status=states.SUCCESS,
                        result=f"""
                            Updated book: {book.title};
                            Unlocked: {bookchaps[-1]['unlocked']}
                            Locked: {bookchaps[-1]['locked']}
                            Loked_from: {bookchaps[-1]['locked_from']}
                            Loked_from_id: {bookchaps[-1]['locked_from_id']}
                        """,
                    )
                elif to_visit == 'boxnovel':
                    pass
            except Exception as exc:
                save_celery_result(
                    task_id=self.request.id,
                    task_name=self.name,
                    status=states.FAILURE,
                    result=exc,
                    traceback=traceback.format_exc(),
                )
                raise Ignore()
        else:
            raise Ignore()
