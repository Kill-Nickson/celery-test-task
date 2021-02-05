web: gunicorn test_task.wsgi --log-file -
django: python manage.py makemigrations
django: python manage.py migrate
worker : celery -A test_task worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
