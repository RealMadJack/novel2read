release: python manage.py collectstatic --noinput
release: python manage.py migrate
web: gunicorn config.wsgi:application
worker: celery -A novel2read.taskapp worker -l info --concurrency=2
beat: celery -A novel2read.taskapp beat -l info -S django
worker_plus_beat: celery -A novel2read.taskapp worker --beat -l info
