from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# setting the Django settings module.
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_rpa.settings')
app = Celery('config')
app.config_from_object(settings, namespace='CELERY')

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()

app.conf.beat_schedule = {}

from rpa import tasks