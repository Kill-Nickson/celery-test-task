web: gunicorn test_task.wsgi --log-file -
celery: celery -A test_task worker -l info
