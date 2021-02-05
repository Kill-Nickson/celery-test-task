web: gunicorn test_task.wsgi --log-file - & celery -A test_task worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo & wait -n
