import os
from celery import Celery
from django.conf import settings
# from celery.schedules import crontab
from datetime import timedelta





os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Warsaw')

app.config_from_object(settings, namespace='CELERY')

# Celery beat settings
app.conf.beat_schedule = {
 
    'download-synoptic-data-every-half-hour': {
        'task': 'weatherapp.tasks.get_api_data',
        'schedule': timedelta(minutes=30),
    },
}


app.autodiscover_tasks()

