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
        self.user_1.profile.votes = 1
        self.user_1.save()

    def test_update_users_votes_task(self):
        self.assertEqual(self.user.profile.votes, 3)
        self.assertEqual(self.user_1.profile.votes, 1)
        update_users_votes.apply().get()
        user = User.objects.get(username='testuser')
        user_1 = User.objects.get(username='testuser-1')
        self.assertEqual(user.profile.votes, 6)
        self.assertEqual(user.profile.premium, True)
        self.assertEqual(user_1.profile.votes, 3)
        self.assertEqual(user_1.profile.premium, False)
