from novel2read.taskapp.celery import app
from django.contrib.auth import get_user_model

User = get_user_model()


@app.task(bind=True)
def update_users_votes(self):
    users = User.objects.all()
    user_prem = users.filter(profile__premium=True)
    user_notprem = users.filter(profile__premium=False)
    user_prem.update(profile__votes=3)
    user_notprem.update(profile__votes=6)
