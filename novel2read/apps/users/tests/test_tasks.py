from django.test import TestCase
from django.contrib.auth import get_user_model

from ..tasks import update_users_votes

User = get_user_model()


class UserTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test')
        self.user_1 = User.objects.create_user(username='testuser-1', password='test-1')
        self.user.profile.premium = True
        self.user.save()

    def test_update_users_votes_task(self):
        resp = update_users_votes.apply().get()
        print(resp)
