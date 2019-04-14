from django.test import TestCase
from django_celery_results.models import TaskResult
from .celery import save_celery_result


class TestCeleryApp(TestCase):
    def setUp(self):
        pass

    def test_save_celery_result(self):
        save_celery_result(123, 'test task', 'success')
        results = TaskResult.objects.all()
        self.assertEqual(results.count(), 1)
        results = results.first()
        self.assertEqual(results.task_id, 123)
        self.assertEqual(results.task_name, 'test task')
        self.assertEqual(results.status, 'success')
