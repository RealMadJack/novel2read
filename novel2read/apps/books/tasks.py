# from celery.result import AsyncResult
# from celery import states
# from celery.exceptions import Ignore
from novel2read.taskapp.celery import app


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

    save_celery_result(self.request.id, self.name)
    """
    print(f"task every 10 sec")
