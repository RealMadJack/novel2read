from novel2read.taskapp.celery import app


@app.task(bind=True)
def update_users_votes(self):
    pass
