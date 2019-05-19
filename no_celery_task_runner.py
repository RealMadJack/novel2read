import logging
import time
import sys
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()


from django_celery_beat.models import PeriodicTask


class TaskRunner:
    def __init__(self):
        logging.info(f'Creating instance: {self.__class__.__name__}')

    def get_django_time_now(self):
        pass

    def get_periodic_tasks(self):
        tasks = PeriodicTask.objects.all()
        print(tasks)

    def run(self):
        sleep_interval = 5
        while True:
            try:
                self.get_periodic_tasks()

                logging.info(f'Writing entries...')
                time.sleep(sleep_interval)
            except KeyboardInterrupt:
                sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)-24s: %(levelname)-8s %(message)s')

    task_runner = TaskRunner()
    task_runner.run()
