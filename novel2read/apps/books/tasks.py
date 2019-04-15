from celery import states
from celery.exceptions import Ignore
from novel2read.taskapp.celery import app

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
def book_scraper_initial(self, book_id):
    """
    get book info
    get book available chapters
    """
    book = Book.objects.get(pk=book_id)
    if book.id_wn:
        pass
    elif book.id_bn:
        pass
    else:
        self.update_state(
            state=states.FAILURE,
            meta='Book id was not specified',
        )
        raise Ignore()


@app.task(bind=True)
def book_scraper_update_info(self):
    """
    get-update book info
    """
    pass


@app.task(bind=True)
def book_scraper_update_chaps(self):
    """
    get-update for new book chapters
    """
    pass
