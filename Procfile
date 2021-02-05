web: gunicorn test_task.wsgi --log-file -
celery: celery -A test_task worker --loglevel=INFO --concurrency=10 -n worker1
