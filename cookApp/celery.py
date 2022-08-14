from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cookApp.settings')

app = Celery('cookApp')
app.conf.enable_utc=False
app.conf.update(timezone='Europe/Kiev')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'Send_mail_every_saturday': {
        'task': 'sendmail.tasks.send_top_5_recipes',
        'schedule': crontab(hour=10, minute=30, day_of_week='saturday')
    },
}

app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
