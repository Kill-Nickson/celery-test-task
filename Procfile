web: gunicorn test_task.wsgi --log-file -
release: python3 manage.py migrate
worker: celery -A test_task worker -B --loglevel=info
