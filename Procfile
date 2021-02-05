web: gunicorn test_task.wsgi --log-file -
worker: celery -A test_task worker -l info
