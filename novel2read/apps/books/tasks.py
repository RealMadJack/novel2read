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
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta=ex,
        )
        raise Ignore()


@app.task(bind=True)
def book_scraper_update(self):
    """
    Divide task
        book_scraper_info
        book_scraper_chaps
        book_scraper_chaps_initial
        pass queryset with different book filters
        async object(1) - task - que
        chain: filter books - substitute
    """
    try:
        qs = Book.objects.all()
        scraper = BookScraper()
        f_books = scraper.get_filter_db_books(qs)
        print(f_books)
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta=ex,
        )
        raise Ignore()


@app.task(bind=True)
def book_scraper_initial(self, book_id, s_to=0):
    """
    TODO: smart_scraper(book, url)
          if book.visit == 'webnovel'...
    """
    book = Book.objects.get(pk=book_id)
    if book.visit_id and not book.visited:
        try:
            scraper = BookScraper()
            url_bb = scraper.url_bb[book.visit]
            book_url = f'{url_bb}{book.visit_id}'
            # book info
            print('book_data')
            book_data = scraper.wn_get_book_data(book_url)
            # print(book_data)
            scraper.update_db_book_data(book, book_data)
            # book chapters
            # c_ids = scraper.wn_get_book_cids(book_url)
            # if book.chapters_count: start_from:
            # bookchaps = scraper.wn_get_book_chaps(book_url, c_ids)
            # scraper.create_update_db_book_chaps(book, bookchaps)
            print('saving visited')
            book.visited = True
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
def book_scraper_update_info(self):
    """
    get-update book info
    """
    self.update_state(
        state=states.FAILURE,
        meta=f'Book id was not specified for book - {book.title}',
    )


@app.task(bind=True)
def book_scraper_update_chaps(self):
    """
    get-update for new book chapters
    """
    pass
