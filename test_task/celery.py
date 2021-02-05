import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')

app = Celery('test_task')

app.conf.update(BROKER_URL='redis://redis-django-data-generator-10183276:2bjYomapBjEYw3LJhRaipfh3gqEcsrZc@redis-10244.c10.us' \
                    '-east-1-2.ec2.cloud.redislabs.com:10244 ',
                CELERY_RESULT_BACKEND='redis://redis-django-data-generator-10183276:2bjYomapBjEYw3LJhRaipfh3gqEcsrZc@redis-10244.c10.us' \
                    '-east-1-2.ec2.cloud.redislabs.com:10244 ')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
