from novel2read.taskapp.celery import app, save_celery_result


@app.task(bind=True)
def debug_task_test(self):
    print(f"task every 10 sec")
    return "task every 10 sec"
