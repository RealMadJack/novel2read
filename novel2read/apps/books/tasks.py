from celery import states
from celery.exceptions import Ignore
from novel2read.taskapp.celery import app
from .models import Book


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
"""
@receiver(post_save, sender=Book)
def update_book_ranking(sender, instance, created=False, **kwargs):
    if created:
        books = Book.objects.published().order_by('-votes')
        # books.update(ranking=0)
        for i, book in enumerate(books, start=1):
            book.ranking = i
            book.save()
"""


@app.task(bind=True)
def update_book_ranking(self):
    try:
        books = Book.objects.published().order_by('-votes')
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta=ex,
        )
        raise Ignore()
