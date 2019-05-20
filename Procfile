release: python manage.py collectstatic --noinput
release: python manage.py migrate
web: gunicorn config.wsgi:application
worker: celery -A novel2read.taskapp worker -l info -B -E
