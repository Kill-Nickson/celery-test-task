web: gunicorn test_task.wsgi --log-file -
release: python3 manage.py migrate
worker : celery -A test_task worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
