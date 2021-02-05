web: gunicorn test_task.wsgi --log-file -
worker: celery -A test_task worker -l info

scheduler: python test_task/manage.py celeryd -B -E --settings=settings.prod
worker: python project/manage.py celeryd -E --settings=settings.prod
