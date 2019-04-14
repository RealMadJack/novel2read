from novel2read.taskapp.celery import app
from django.contrib.auth import get_user_model

User = get_user_model()


@app.task(bind=True)
def update_users_votes(self):
    users = User.objects.all()
    user_prem = users.filter(profile__premium=True)
    user_nonprem = users.filter(profile__premium=False)
    try:
        user_prem.update(profile__votes=3)
        user_nonprem.update(profile__votes=6)
    except Exception as ex:
        raise ex
