from celery import states
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..tasks import update_users_votes

User = get_user_model()


class UserTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test')
        self.user_1 = User.objects.create_user(username='testuser-1', password='test-1')
        self.user.profile.premium = True
        self.user.save()
        self.user_1.profile.votes = 1
        self.user_1.save()

    def test_update_users_votes_task(self):
        self.assertEqual(self.user.profile.votes, 3)
        self.assertEqual(self.user_1.profile.votes, 1)
        res = update_users_votes.apply()
        self.user.refresh_from_db()
        self.user_1.refresh_from_db()
        self.assertEqual(res.state, states.SUCCESS)
        self.assertEqual(self.user.profile.votes, 6)
        self.assertEqual(self.user.profile.premium, True)
        self.assertEqual(self.user_1.profile.votes, 3)
        self.assertEqual(self.user_1.profile.premium, False)
