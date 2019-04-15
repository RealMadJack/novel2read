from celery import states
from celery.exceptions import Ignore
from novel2read.taskapp.celery import app
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@app.task(bind=True)
def update_users_votes(self):
    try:
        profiles = Profile.objects.all()
        profiles_prem = profiles.filter(premium=True)
        profiles_nonprem = profiles.filter(premium=False)
        profiles_prem.update(votes=6)
        profiles_nonprem.update(votes=3)
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta=ex,
        )
        raise Ignore()
