import os
from celery import Celery, Task
from celery.result import AsyncResult
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.local"
    )  # pragma: no cover


app = Celery("novel2read")
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


class CeleryAppConfig(AppConfig):
    name = "novel2read.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


class RequestBaseTask(Task):
    def run(self, *args, **kwargs):
        # The body of the task executed by workers. Required.
        pass

    def on_success(self, retval, task_id, *args, **kwargs):
        # do something with usefull values as retval and task_id
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # do something
        pass


def save_celery_result(task_id='', task_name='', status='', *args, **kwargs):
    from django_celery_results.models import TaskResult
    try:
        TaskResult.objects.create(task_id=task_id, task_name=task_name, status=status)
    except Exception as e:
        raise e


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
